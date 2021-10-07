---
title: Code Reading - Open component in editor - vue-devtools
date: 2021-10-07 17:09
author: Sim
tags: Javascript, vue, vue-devtools, compatibility, node
summary: It's a browser devtools extension for debugging Vue.js applications
---

Thank [Ruochuan](https://lxchuan12.gitee.io) for hosting [this](https://yuque.com/ruochuan12) and [his doc](https://github.com/lxchuan12/open-in-editor).
I'm never a fan of reading others' source code, now I can read with them.

Project: @github:vuejs/devtools

## Prerequisition

1. initiate a vue project
```
# globally install cue-cli
yarn global add @vue/cli
# create a cue 3 project
vue create vue3-project
```
2. install a vue-devtools on the browser.

## Actions

++f12++ for the dev tool.
Switch to `Vue` tab, then open the component in editor.

![](https://snorl.ax/posts/2021-10-07-19-29-47.png)

Then a component is opened in my vscode editor.

## What happened

A GET request was issued to `/__open-in-editor?file=src/components/HelloWorld.vue`, as is shown in the pic:
![](https://snorl.ax/posts/2021-10-07-19-31-27.png)

### GET API logic

So I included `**/node_modules` in the search scope in vscode, then searched the vue project for `/__open-in-editor`, then I found the following code.

#### `node_modules/@vue/cli-service/lib/commands/serve.js`

```{js hl_lines="26"}
    const launchEditorMiddleware = require('launch-editor-middleware')
    // ...
    const server = new WebpackDevServer(compiler, Object.assign({
      logLevel: 'silent',
      clientLogLevel: 'silent',
      historyApiFallback: {
        disableDotRule: true,
        rewrites: genHistoryApiFallbackRewrites(options.publicPath, options.pages)
      },
      contentBase: api.resolve('public'),
      watchContentBase: !isProduction,
      hot: !isProduction,
      injectClient: false,
      compress: isProduction,
      publicPath: options.publicPath,
      overlay: isProduction // TODO disable this
        ? false
        : { warnings: false, errors: true }
    }, projectDevServerOptions, {
      https: useHttps,
      proxy: proxySettings,
      // eslint-disable-next-line no-shadow
      before (app, server) {
        // launch editor support.
        // this works with vue-devtools & @vue/cli-overlay
        app.use('/__open-in-editor', launchEditorMiddleware(() => console.log(
          `To specify an editor, specify the EDITOR env variable or ` +
          `add "editor" field to your Vue project config.\n`
        )))
        // allow other plugins to register middlewares, e.g. PWA
        api.service.devServerConfigFns.forEach(fn => fn(app, server))
        // apply in project middlewares
        projectDevServerOptions.before && projectDevServerOptions.before(app, server)
      },
      // avoid opening browser
      open: false
    }))
```

The package `launch-editor-middleware` is crucial here for handling the actions.

### node package - `launch-editor-middleware`

#### `node_modules/launch-editor-middleware/index.js`

```js
const url = require('url')
const path = require('path')
const launch = require('launch-editor')

module.exports = (specifiedEditor, srcRoot, onErrorCallback) => {
  if (typeof specifiedEditor === 'function') {
    onErrorCallback = specifiedEditor
    specifiedEditor = undefined
  }

  if (typeof srcRoot === 'function') {
    onErrorCallback = srcRoot
    srcRoot = undefined
  }

  srcRoot = srcRoot || process.cwd()

  return function launchEditorMiddleware (req, res, next) {
    const { file } = url.parse(req.url, true).query || {}
    if (!file) {
      res.statusCode = 500
      res.end(`launch-editor-middleware: required query param "file" is missing.`)
    } else {
      launch(path.resolve(srcRoot, file), specifiedEditor, onErrorCallback)
      res.end()
    }
  }
}
```

So basically in the `serve.js`, the default exported function is called with the first argument assigned to a `console.log` callback (the other 2 r undefined), meaning:
1. it will print the corresponding messages to the console on error (the callback assigned to the variable `onErrorCallback`).
2. `specifiedEditor` is undefined, which is falsy
3. `srcRoot` is the returned value of `process.cwd()`, which is the path of the current working directory.
4. in the end, it returns a function, which will try to find the value of the querystring `file`, then execute `launch` with the full path of it, `specifiedEditor` and `onErrorCallback` as arguments.
   
The `launch` is imported from the package `launch-editor`.

### node package - `launch-editor`

#### `node_modules/launch-editor/index.js`

```{js hl_lines="20-37 50-60 65 78 80"}
/**
 * Copyright (c) 2015-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file at
 * https://github.com/facebookincubator/create-react-app/blob/master/LICENSE
 *
 * Modified by Yuxi Evan You
 */

const fs = require('fs')
const os = require('os')
const path = require('path')
const chalk = require('chalk')
const childProcess = require('child_process')

const guessEditor = require('./guess')
const getArgumentsForPosition = require('./get-args')

function wrapErrorCallback (cb) {
  return (fileName, errorMessage) => {
    console.log()
    console.log(
      chalk.red('Could not open ' + path.basename(fileName) + ' in the editor.')
    )
    if (errorMessage) {
      if (errorMessage[errorMessage.length - 1] !== '.') {
        errorMessage += '.'
      }
      console.log(
        chalk.red('The editor process exited with an error: ' + errorMessage)
      )
    }
    console.log()
    if (cb) cb(fileName, errorMessage)
  }
}

function isTerminalEditor (editor) {
  switch (editor) {
    case 'vim':
    case 'emacs':
    case 'nano':
      return true
  }
  return false
}

const positionRE = /:(\d+)(:(\d+))?$/
function parseFile (file) {
  const fileName = file.replace(positionRE, '')
  const match = file.match(positionRE)
  const lineNumber = match && match[1]
  const columnNumber = match && match[3]
  return {
    fileName,
    lineNumber,
    columnNumber
  }
}

let _childProcess = null

function launchEditor (file, specifiedEditor, onErrorCallback) {
  const parsed = parseFile(file)
  let { fileName } = parsed
  const { lineNumber, columnNumber } = parsed

  if (!fs.existsSync(fileName)) {
    return
  }

  if (typeof specifiedEditor === 'function') {
    onErrorCallback = specifiedEditor
    specifiedEditor = undefined
  }

  onErrorCallback = wrapErrorCallback(onErrorCallback)

  const [editor, ...args] = guessEditor(specifiedEditor)
  if (!editor) {
    onErrorCallback(fileName, null)
    return
  }

  if (
    process.platform === 'linux' &&
    fileName.startsWith('/mnt/') &&
    /Microsoft/i.test(os.release())
  ) {
    // Assume WSL / "Bash on Ubuntu on Windows" is being used, and
    // that the file exists on the Windows file system.
    // `os.release()` is "4.4.0-43-Microsoft" in the current release
    // build of WSL, see: https://github.com/Microsoft/BashOnWindows/issues/423#issuecomment-221627364
    // When a Windows editor is specified, interop functionality can
    // handle the path translation, but only if a relative path is used.
    fileName = path.relative('', fileName)
  }

  if (lineNumber) {
    const extraArgs = getArgumentsForPosition(editor, fileName, lineNumber, columnNumber)
    args.push.apply(args, extraArgs)
  } else {
    args.push(fileName)
  }

  if (_childProcess && isTerminalEditor(editor)) {
    // There's an existing editor process already and it's attached
    // to the terminal, so go kill it. Otherwise two separate editor
    // instances attach to the stdin/stdout which gets confusing.
    _childProcess.kill('SIGKILL')
  }

  if (process.platform === 'win32') {
    // On Windows, launch the editor in a shell because spawn can only
    // launch .exe files.
    _childProcess = childProcess.spawn(
      'cmd.exe',
      ['/C', editor].concat(args),
      { stdio: 'inherit' }
    )
  } else {
    _childProcess = childProcess.spawn(editor, args, { stdio: 'inherit' })
  }
  _childProcess.on('exit', function (errorCode) {
    _childProcess = null

    if (errorCode) {
      onErrorCallback(fileName, '(code ' + errorCode + ')')
    }
  })

  _childProcess.on('error', function (error) {
    onErrorCallback(fileName, error.message)
  })
}

module.exports = launchEditor
```

1. `file` is parsed by `parseFile`, returning corresponding `filename`, `lineNumber`, `columnNumber`
2. `onErrorCallback` is wrapped by `wrapErrorCallback`, returning a function for printing error messages of a file (accepting `fileName` and `errorMessage` as arguments), where `onErrorCallback` is used to print the trailing error messages, following `Could not open ${filename} in the editor.`, `The editor process exited with an error: ${parsedErrorMessage}` (if `errorMessage` is truthy). 
3. `specifiedEditor` is parsed by `guessEditor`, which is located in `guess.js` in the same package

If `editor` from `guessEditor` is falsy, it will call `onErrorCallback` with `fileName` and a falsy `errorMessage`, then the function returns nothing.
If it's on a WSL, `fileName` needs conversion.
If `lineNumber` is truthy, the results returned from `getArgumentsForPosition` (located in `./args.js`, the function basically is a dictionary for handling different argument grammers of different editors) will be used as extra arguments.
If a `_childProcess` was created by this tool before in this session and the `editor` obtained this time is a terminal editor, the previous `_childProcess` will be killed.
Then finally, the editor will be called with the arguments, the command is slightly different according to the platform (`win32` vs unix ones). The process will be assigned to `_childProcess`.
Also, the `_childProcess` will call `onErrorCallback` on error (also the case when an error returned from exiting).

#### `node_modules/launch-editor/guess.js`

```js
const path = require('path')
const shellQuote = require('shell-quote')
const childProcess = require('child_process')

// Map from full process name to binary that starts the process
// We can't just re-use full process name, because it will spawn a new instance
// of the app every time
const COMMON_EDITORS_OSX = require('./editor-info/osx')
const COMMON_EDITORS_LINUX = require('./editor-info/linux')
const COMMON_EDITORS_WIN = require('./editor-info/windows')

module.exports = function guessEditor (specifiedEditor) {
  if (specifiedEditor) {
    return shellQuote.parse(specifiedEditor)
  }
  // We can find out which editor is currently running by:
  // `ps x` on macOS and Linux
  // `Get-Process` on Windows
  try {
    if (process.platform === 'darwin') {
      const output = childProcess.execSync('ps x').toString()
      const processNames = Object.keys(COMMON_EDITORS_OSX)
      for (let i = 0; i < processNames.length; i++) {
        const processName = processNames[i]
        if (output.indexOf(processName) !== -1) {
          return [COMMON_EDITORS_OSX[processName]]
        }
      }
    } else if (process.platform === 'win32') {
      const output = childProcess
        .execSync('powershell -Command "Get-Process | Select-Object Path"', {
          stdio: ['pipe', 'pipe', 'ignore']
        })
        .toString()
      const runningProcesses = output.split('\r\n')
      for (let i = 0; i < runningProcesses.length; i++) {
        // `Get-Process` sometimes returns empty lines
        if (!runningProcesses[i]) {
          continue
        }

        const fullProcessPath = runningProcesses[i].trim()
        const shortProcessName = path.basename(fullProcessPath)

        if (COMMON_EDITORS_WIN.indexOf(shortProcessName) !== -1) {
          return [fullProcessPath]
        }
      }
    } else if (process.platform === 'linux') {
      // --no-heading No header line
      // x List all processes owned by you
      // -o comm Need only names column
      const output = childProcess
        .execSync('ps x --no-heading -o comm --sort=comm')
        .toString()
      const processNames = Object.keys(COMMON_EDITORS_LINUX)
      for (let i = 0; i < processNames.length; i++) {
        const processName = processNames[i]
        if (output.indexOf(processName) !== -1) {
          return [COMMON_EDITORS_LINUX[processName]]
        }
      }
    }
  } catch (error) {
    // Ignore...
  }

  // Last resort, use old skool env vars
  if (process.env.VISUAL) {
    return [process.env.VISUAL]
  } else if (process.env.EDITOR) {
    return [process.env.EDITOR]
  }

  return [null]
}
```

In this case, `specifiedEditor` is falsy, so the process first lists the running processes in the defined logic, which is different on different platforms:
1. in `darwin`, it gets the output of `ps x`
2. in `win32`, it gets the output of `powershell -Command "Get-Process | Select-Object Path`
3. in `linux`, it gets the output of `ps x --no-heading -o comm --sort=comm`

Then it tries to find a editor from its predefined dictionary with common editors on the platform and returns it
When it fails to find any on the dictionary, it will try to refer to environmental variables `VISUAL` and `EDITOR` and return either of them (when both is present, `VISUAL` is preferred)
When it still fails to return any, it will return an empty result.

#### `node_modules/launch-editor/get-args.js`

```
const path = require('path')

// normalize file/line numbers into command line args for specific editors
module.exports = function getArgumentsForPosition (
  editor,
  fileName,
  lineNumber,
  columnNumber = 1
) {
  const editorBasename = path.basename(editor).replace(/\.(exe|cmd|bat)$/i, '')
  switch (editorBasename) {
    case 'atom':
    case 'Atom':
    case 'Atom Beta':
    case 'subl':
    case 'sublime':
    case 'sublime_text':
    case 'wstorm':
    case 'charm':
      return [`${fileName}:${lineNumber}:${columnNumber}`]
    case 'notepad++':
      return ['-n' + lineNumber, fileName]
    case 'vim':
    case 'mvim':
      return [`+call cursor(${lineNumber}, ${columnNumber})`, fileName]
    case 'joe':
      return ['+' + `${lineNumber}`, fileName]
    case 'emacs':
    case 'emacsclient':
      return [`+${lineNumber}:${columnNumber}`, fileName]
    case 'rmate':
    case 'mate':
    case 'mine':
      return ['--line', lineNumber, fileName]
    case 'code':
    case 'code-insiders':
    case 'Code':
      return ['-r', '-g', `${fileName}:${lineNumber}:${columnNumber}`]
    case 'appcode':
    case 'clion':
    case 'clion64':
    case 'idea':
    case 'idea64':
    case 'phpstorm':
    case 'phpstorm64':
    case 'pycharm':
    case 'pycharm64':
    case 'rubymine':
    case 'rubymine64':
    case 'webstorm':
    case 'webstorm64':
      return ['--line', lineNumber, fileName]
  }

  // For all others, drop the lineNumber until we have
  // a mapping above, since providing the lineNumber incorrectly
  // can result in errors or confusing behavior.
  return [fileName]
}
```

Basically a dictionary for handling different argument grammers of different editors

## What I learned

1. well a lotta compatibility things, ex. running process searching command, `ps x` on unix ones, `powershell -Command`. I guess I can utilize the code when doing a node application needing compatibilities on both unix and windows platforms
2. file handing in node applications
3. I can open component in my current editor just via a GET API? nice. It's really convenient in local Vue project development