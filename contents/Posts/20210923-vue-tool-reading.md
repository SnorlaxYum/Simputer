---
title: Code Reading - Shared Tool in vue-next
date: 2021-09-24 18:09
author: Sim
tags: Javascript, vue, vue-next, node
summary: Well, the code is not long. Nice for my source code reading journey.
---

Thank [Ruochuan](https://lxchuan12.gitee.io) for hosting [this](https://yuque.com/ruochuan12).
I'm never a fan of reading others' source code, now I can read with them.

Project: @github:vuejs/vue-next
[Source Code](https://github.com/vuejs/vue-next/blob/master/packages/shared/src/index.ts)

## Things in it

### babelParserDefaultPlugins

#### Code

```ts
/**
 * List of @babel/parser plugins that are used for template expression
 * transforms and SFC script transforms. By default we enable proposals slated
 * for ES2020. This will need to be updated as the spec moves forward.
 * Full list at https://babeljs.io/docs/en/next/babel-parser#plugins
 */
export const babelParserDefaultPlugins = [
  'bigInt',
  'optionalChaining',
  'nullishCoalescingOperator'
] as const
```

As the comment says, `@babel/parser` plugins. By default vue uses `bigInt`, `optionalChaining` and `nullishCoalescingOperator`

#### What it does

used for babel parsing plugins argument
ex. `packages/compiler-core/src/utils.ts`

### Empty Things

#### Code

```ts
// empty object
export const EMPTY_OBJ: { readonly [key: string]: any } = __DEV__
  ? Object.freeze({})
  : {}
// empty array
export const EMPTY_ARR = __DEV__ ? Object.freeze([]) : []

// empty function
export const NOOP = () => {}

/**
 * Always return false.
 */
export const NO = () => false
```

#### What they do

NOOP: empty fallback for function
EMPTY_OBJ: empty fallback for object
ex. `packages/compiler-core/src/transform.ts`

EMPTY_ARR: empty fallback for array
ex. `packages/runtime-core/src/vnode.ts`

NO: fallback function returning false.
ex. `packages/compiler-ssr/src/transforms/ssrTransformElement.ts`

### Event Finders

#### Code

```ts
// onXXX
const onRE = /^on[^a-z]/
export const isOn = (key: string) => onRE.test(key)

// onUpdate:
export const isModelListener = (key: string) => key.startsWith('onUpdate:')
```

#### What they do

isOn: onXXX judge
isModelListener: update the model if it begins with `onUpdate`
ex. `packages/runtime-dom/src/patchProp.ts`

### extend

#### Code

```ts
export const extend = Object.assign
```

#### What it does

extend: extend the option with the extra one
ex. `packages/reactivity/src/effect.ts`

### remove

#### Code

```ts
export const remove = <T>(arr: T[], el: T) => {
  const i = arr.indexOf(el)
  if (i > -1) {
    arr.splice(i, 1)
  }
}
```

#### What it does

remove: remove the el from the array
ex. `packages/runtime-core/src/components/KeepAlive.ts`

### hasOwn

#### Code

```ts
const hasOwnProperty = Object.prototype.hasOwnProperty
export const hasOwn = (
  val: object,
  key: string | symbol
): key is keyof typeof val => hasOwnProperty.call(val, key)
```

#### What it does

hasOwn: a wrapper for Object.prototype.hasOwnPreperty
ex. `packages/runtime-core/src/componentEmits.ts`

### Type Assertion And Conversion related things

#### Code

```ts
// makeMap (imported from packages/shared/src/makeMap.ts)
// function makeMap(
//   str: string,
//   expectsLowerCase?: boolean
// ): (key: string) => boolean {
//   const map: Record<string, boolean> = Object.create(null)
//   const list: Array<string> = str.split(',')
//   for (let i = 0; i < list.length; i++) {
//     map[list[i]] = true
//   }
//   return expectsLowerCase ? val => !!map[val.toLowerCase()] : val => !!map[val]
// }
export const isArray = Array.isArray
export const isMap = (val: unknown): val is Map<any, any> =>
  toTypeString(val) === '[object Map]'
export const isSet = (val: unknown): val is Set<any> =>
  toTypeString(val) === '[object Set]'

export const isDate = (val: unknown): val is Date => val instanceof Date
export const isFunction = (val: unknown): val is Function =>
  typeof val === 'function'
export const isString = (val: unknown): val is string => typeof val === 'string'
export const isSymbol = (val: unknown): val is symbol => typeof val === 'symbol'
export const isObject = (val: unknown): val is Record<any, any> =>
  val !== null && typeof val === 'object'

export const isPromise = <T = any>(val: unknown): val is Promise<T> => {
  return isObject(val) && isFunction(val.then) && isFunction(val.catch)
}

export const objectToString = Object.prototype.toString
export const toTypeString = (value: unknown): string =>
  objectToString.call(value)

export const toRawType = (value: unknown): string => {
  // extract "RawType" from strings like "[object RawType]"
  return toTypeString(value).slice(8, -1)
}

export const isPlainObject = (val: unknown): val is object =>
  toTypeString(val) === '[object Object]'

export const isIntegerKey = (key: unknown) =>
  isString(key) &&
  key !== 'NaN' &&
  key[0] !== '-' &&
  '' + parseInt(key, 10) === key

export const isReservedProp = /*#__PURE__*/ makeMap(
  // the leading comma is intentional so empty string "" is also included
  ',key,ref,' +
    'onVnodeBeforeMount,onVnodeMounted,' +
    'onVnodeBeforeUpdate,onVnodeUpdated,' +
    'onVnodeBeforeUnmount,onVnodeUnmounted'
)
```

#### What isReservedProp does

Most of them r self-explainary. So I'd only focus on the `isReservedProp` which utilizes its self-created `makeMap`.
`makeMap` overall does this: split the string into an array of string, then put them into a Map as keys with all the values set to `true`, finally returns a function expected to return a boolean indicating whether a string exists in this Map. If a second truthy argument is given to `makeMap`, the function will convert the given string into lower case and return the result.
So basically `isReservedProp` is a function returning true only if the given string is one of these: `""`, `"key"`, `"ref"`, `"onVnodeBeforeMount"`, `"onVnodeMounted"`, `"onVnodeBeforeUpdate"`, `"onVnodeUpdated"`, `"onVnodeBeforeUnmount"`, `"onVnodeUnmounted"`.

ex. `packages/runtime-core/src/compat/renderHelpers.ts`

### cacheStringFunction

#### Code

```ts
const cacheStringFunction = <T extends (str: string) => string>(fn: T): T => {
  const cache: Record<string, string> = Object.create(null)
  return ((str: string) => {
    const hit = cache[str]
    return hit || (cache[str] = fn(str))
  }) as any
}
```

#### What it does

`cacheStringFunction` is a function doing this:
1. receives a function returning a corresponding record using the given key string
2. creates a cache object
3. returns a function doing this:
   1. trying to get the record from the cache using the given key, returns it if it's a truthy string
   2. if it fails to get the record, it will add the record returned from the given function to the cache object and returns the added record.

It is not exported because it is only used by the string dealing functions in the [following section](#string-dealing).

### String Dealing

#### Code

```ts
const camelizeRE = /-(\w)/g
/**
 * @private
 */
export const camelize = cacheStringFunction((str: string): string => {
  return str.replace(camelizeRE, (_, c) => (c ? c.toUpperCase() : ''))
})

const hyphenateRE = /\B([A-Z])/g
/**
 * @private
 */
export const hyphenate = cacheStringFunction((str: string) =>
  str.replace(hyphenateRE, '-$1').toLowerCase()
)

/**
 * @private
 */
export const capitalize = cacheStringFunction(
  (str: string) => str.charAt(0).toUpperCase() + str.slice(1)
)

/**
 * @private
 */
export const toHandlerKey = cacheStringFunction((str: string) =>
  str ? `on${capitalize(str)}` : ``
)
```

#### What they do

`camelize`: camelize a string, ex. `some-thing` into `someThing`
`hyphenate`: hyphenate a string, ex. `someThing` into `some-thing`
`capitalize`: capitalize a string, ex. `something` into `Something`
`toHanlderKey`: convert an event name into a handler attr used in somewhere like jsx, ex. `click` into `onClick`

They all utilize `cacheStringFunction`, so for the same key, the result will be returned from the calulating function on the first time, from the inner cache object after that.

### hasChanged

#### Code

```ts
// compare whether a value has changed, accounting for NaN.
export const hasChanged = (value: any, oldValue: any): boolean =>
  !Object.is(value, oldValue)
```

#### What it does

defines if 2 values r the same using [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is).
(Notice: for 0, it will only return true when both r of the same sign)

### invokeArrayFns

#### Code

```ts
export const invokeArrayFns = (fns: Function[], arg?: any) => {
  for (let i = 0; i < fns.length; i++) {
    fns[i](arg)
  }
}
```

#### What it does

invoke the functions in the array.
usually used in hooks.

### def

#### Code

```ts
export const def = (obj: object, key: string | symbol, value: any) => {
  Object.defineProperty(obj, key, {
    configurable: true,
    enumerable: false,
    value
  })
}
```

#### What it does

define a property named the given `key` on the given `obj` with the given `value`.
ex. used in `packages/runtime-core/src/componentProps.ts`

### toNumber

#### Code

```ts
export const toNumber = (val: any): any => {
  const n = parseFloat(val)
  return isNaN(n) ? val : n
}
```

#### What it does

converts the given value to a number, returns:
1. the converted value if it is not NaN
2. the original value if it is NaN

ex. used in `packages/runtime-dom/src/components/Transition.ts`

### getGlobalThis

#### Code

```ts
let _globalThis: any
export const getGlobalThis = (): any => {
  return (
    _globalThis ||
    (_globalThis =
      typeof globalThis !== 'undefined'
        ? globalThis
        : typeof self !== 'undefined'
        ? self
        : typeof window !== 'undefined'
        ? window
        : typeof global !== 'undefined'
        ? global
        : {})
  )
}
```

#### What it does

returns the global environment where the code is executed (returns from the calculation function on the first time, from the `_globalThis` afterwards)
ex. used in `packages/runtime-core/src/renderer.ts` to add required props and values to the global environment.

## What I got from it

1. sometimes caching necessary for getting the required values, (ex. `_globalThis`, `cacheStringFunction`)
2. though we have things declared in the default js, it's nice to store them into shortcut variables for our own convenience
3. `Object.is` is an excellent alternative to `===`, with the additional condition judging if the given 0s have the same sign
4. I guess this tool can be really utilized when I need something like type assertion, camleization in my application