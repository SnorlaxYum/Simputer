---
title: Notes on MDN Web Docs Javascript Guide
date: 2019-05-23 22:08
modified: 2019-05-27 12:28
author: Sim
tags: MDN, javascript, learning notes
status: published
summary: Looks like that it suits me much when it comes to learning js.  
---

After learning from YDJS for a while, I did some practice. At first I searched for some ideas, and then I decided to do a clock[^1].  

Then you can see it on the home page of the site[^2], with the image changing every 5 seconds randomly. In the origin project, `setTimeout` seems to be a viable choice. But when it comes to two different elements that need different intervals, `setInterval` comes in handy. `setTimeout` won't support two functions with different intervals. That's what I experienced. They both serve as js timing functions[^3]. Now I prefer `setInterval`.  

Anyway, it might be too early for me to start with YDJS, though it's a good book. So I decided to switch to MDN Web Docs[^4] instead.  

I only takes what seems new to me 'cause it seems that I've been acquiainted with many of the contents.

## Grammer and Types

Multiple lines usage in string literals:  

```js
var poem =
'Roses are red,\n\
Violets are blue.\n\
Sugar is sweet,\n\
and so is foo.'
```

Template Literals[^5] from ECMAScript 2015 as a new way for multiple lines string literals:  

```js
var poem =
`Roses are red,
Violets are blue.
Sugar is sweet,
and so is foo.`
```

## Control flow and error handling

### Block statement

Starting with ECMAScript2015, the `let` and `const` variable declarations are block scoped.

### `switch` statement

It's almost the same as C.

An exceptional example is located at `switch` section at Chapter 5 in this note[^6].

### Exception handling statements

Throw exceptions: `throw` statement  
Handle exceptions: `try...catch` statement

```js
try {
  something;
} catch (e) {
  something;
} finally {
  finalthing;
}

```

It's similar to this in Python:  

```python
try:
    something
except Exception as e:
    something
finally:
    finalthing
```

`e` is an identifier for the error thrown. `finally` will be executed whether the `e` happens.  

`e` has properties `name` amd `message` in js, similar to `type(e)` and `e.args` in Python.  

### Promises

Starting with ECMAScript2015, JavaScript gains support for Promise objects[^7] allowing you to control the flow of deferred and asynchronous operations.

`imgLoad` example:  

```js
function imgLoad(url) {
  return new Promise(function(resolve, reject) {
    var request = new XMLHttpRequest();
    request.open('GET', url);
    request.responseType = 'blob';
    request.onload = function() {
      if (request.status === 200) {
        resolve(request.response);
      } else {
        reject(Error('Image didn\'t load successfully; error code:'
                     + request.statusText));
      }
    };
    request.onerror = function() {
      reject(Error('There was a network error.'));
    };
    request.send();
  });
}
```

`resolve` when the task succeeds, `reject` otherwise. [^7]

## Loops and iteration

Loops in js:  

* for statement
* do...while statement
* while statement
* labeled statement
* break statement
* continue statement
* for...in statement
* for...of statement

The first 6: Similar to C.
`for .. in`: When used on objects, return all the property names(keys). WHen used in arrays, return from 0 to (array.length - 1)
`for .. of`: When used on objects, return all the property values(values). When used in arrays return from array[0] to array[array.length-1]

## Functions

declarations: name, paramters, statements inside curly brackets. In js, functions can be defined in var form:  

```js
var fun_name = function() {statements;}
```

As I learned from YDJS, function is also a object. With `this`, a var assignment from a function can be assigned property keys and values.

With the needed parameters a function can be executed and complete what has been defined in it.  

Vars defined inside a function has its scope of execution inside.

Things like recursion, nests, no difference from C.

`arguments` is a function-scope var containing a list of parameters passed to the function.

Default parameters: `undefined`, can be set to other values.

### Rest parameters

Example says everything:  

```js
function multiply(multiplier, ...theArgs) {
  return theArgs.map(x => multiplier * x);
}

var arr = multiply(2, 1, 2, 3);
console.log(arr); // [2, 4, 6]
```

### Shorter functions

```js
var a = [
  'Hydrogen',
  'Helium',
  'Lithium',
  'Beryllium'
];

var a2 = a.map(function(s) { return s.length; });

console.log(a2); // logs [8, 6, 7, 9]

var a3 = a.map(s => s.length);

console.log(a3); // logs [8, 6, 7, 9]
```

### No seperate `this`

```js
function Person() {
  // The Person() constructor defines `this` as itself.
  this.age = 0;

  setInterval(function growUp() {
    // In nonstrict mode, the growUp() function defines `this`
    // as the global object, which is different from the `this`
    // defined by the Person() constructor.
    this.age++;
  }, 1000);
}

var p = new Person();
```

Solution:  

```js
function Person() {
  var self = this; // Some choose `that` instead of `self`.
                   // Choose one and be consistent.
  self.age = 0;

  setInterval(function growUp() {
    // The callback refers to the `self` variable of which
    // the value is the expected object.
    self.age++;
  }, 1000);
}
```

Arrow function doesn't have its own `this`, so viable directly:  

```js
function Person() {
  this.age = 0;

  setInterval(() => {
    this.age++; // |this| properly refers to the person object
  }, 1000);
}

var p = new Person();
```

### Predefined functions

`eval()`: The eval() method evaluates JavaScript code represented as a string.  

`uneval()`: The uneval() method creates a string representation of the source code of an Object.

`isFinite()`: The global isFinite() function determines whether the passed value is a finite number. If needed, the parameter is first converted to a number.

`isNaN()`: The isNaN() function determines whether a value is NaN or not. Note: coercion inside the isNaN function has interesting rules; you may alternatively want to use Number.isNaN(), as defined in ECMAScript 2015, or you can use typeof to determine if the value is Not-A-Number.

`parseFloat()`: The parseFloat() function parses a string argument and returns a floating point number.

`parseInt()`: The parseInt() function parses a string argument and returns an integer of the specified radix (the base in mathematical numeral systems).

`decodeURI()`: The decodeURI() function decodes a Uniform Resource Identifier (URI) previously created by encodeURI or by a similar routine.

`decodeURIComponent()`: The decodeURIComponent() method decodes a Uniform Resource Identifier (URI) component previously created by encodeURIComponent or by a similar routine.

`encodeURI()`: The encodeURI() method encodes a Uniform Resource Identifier (URI) by replacing each instance of certain characters by one, two, three, or four escape sequences representing the UTF-8 encoding of the character (will only be four escape sequences for characters composed of two "surrogate" characters).

`encodeURIComponent()`: The encodeURIComponent() method encodes a Uniform Resource Identifier (URI) component by replacing each instance of certain characters by one, two, three, or four escape sequences representing the UTF-8 encoding of the character (will only be four escape sequences for characters composed of two "surrogate" characters).

`escape()`: The deprecated escape() method computes a new string in which certain characters have been replaced by a hexadecimal escape sequence. Use encodeURI or encodeURIComponent instead.

`unescape()`: The deprecated unescape() method computes a new string in which hexadecimal escape sequences are replaced with the character that it represents. The escape sequences might be introduced by a function like escape. Because unescape() is deprecated, use decodeURI() or decodeURIComponent instead.

## Expressions and operators

Assignment Operator: `=`
Compound operators:  `+=`, `<<=`, `>>>=`, `|=` etc.

### Destructuring in assignment

```js
var foo = ['one', 'two', 'three'];

// without destructuring
var one   = foo[0];
var two   = foo[1];
var three = foo[2];

// with destructuring
var [one, two, three] = foo;
```

Comparison operators: `==`, `>=`, `===`, etc.

Arithmetic operators: `%`, `++`, etc.

Bitwise operators: `|`, `&`, `<<` etc.

Logical operators: `&&`, `||`, `!`

String operators: `+`

Conditional operator: `?`

Coma operator:  

```js
var x = [0,1,2,3,4,5,6,7,8,9]
var a = [x, x, x, x, x];

for (var i = 0, j = 9; i <= j; i++, j--)
  console.log('a[' + i + '][' + j + ']= ' + a[i][j]);
```

Unary operators: `delete`, `typeof`, `void`.  

```html
<a href="javascript:void(0)">Click here to do nothing</a>

<a href="javascript:void(document.form.submit())">
Click here to submit</a>
```

#### Relational operators

##### `in`

```js
// Arrays
var trees = ['redwood', 'bay', 'cedar', 'oak', 'maple'];
0 in trees;        // returns true
3 in trees;        // returns true
6 in trees;        // returns false
'bay' in trees;    // returns false (you must specify the index number,
                   // not the value at that index)
'length' in trees; // returns true (length is an Array property)

// built-in objects
'PI' in Math;          // returns true
var myString = new String('coral');
'length' in myString;  // returns true

// Custom objects
var mycar = { make: 'Honda', model: 'Accord', year: 1998 };
'make' in mycar;  // returns true
'model' in mycar; // returns true
```

##### `instanceof`

```js
var theDay = new Date(1995, 12, 17);
if (theDay instanceof Date) {
  // statements to execute
}
```

#### Expressions

Arithmetic: evaluates to a number, for example 3.14159. (Generally uses arithmetic operators.)
String: evaluates to a character string, for example, "Fred" or "234". (Generally uses string operators.)
Logical: evaluates to true or false. (Often involves logical operators.)

##### Primary expressions

Basic keywords and general expressions in JavaScript.

`this`: current object  
`()`: control precedence.

##### Left-hand-side expressions

Left values are the destination of an assignment.

`new`: create an instance.  
`super`: call on objects' parent[^8]  

###### Spread Operator

Use with array:  

```js
var parts = ['shoulders', 'knees'];
var lyrics = ['head', ...parts, 'and', 'toes'];
```

Use with function calls:  

```js
function f(x, y, z) { }
var args = [0, 1, 2];
f(...args);
```

## Numbers and dates

### Numbers

#### Decimal numbers

```js
1234567890
42

// Caution when using leading zeros:

0888 // 888 parsed as decimal
0777 // parsed as octal in non-strict mode (511 in decimal)
```

#### Binary numbers

Leading with `0b` and `0B`:  

```js
var FLT_SIGNBIT  = 0b10000000000000000000000000000000; // 2147483648
var FLT_EXPONENT = 0b01111111100000000000000000000000; // 2139095040
var FLT_MANTISSA = 0B00000000011111111111111111111111; // 8388607
```

#### Octal Numbers

Leading with zeros:  

```js
var n = 0755; // 493
var m = 0644; // 420
```

Leading with `0o`:  

```js
var a = 0o10; // ES2015: 8
```

#### Hexadecimal numbers

Leading with `0x` or `0X`:  

```js
0xFFFFFFFFFFFFFFFFF // 295147905179352830000
0x123456789ABCDEF   // 81985529216486900
0XA                 // 10
```

#### Exponentiation

```js
1E3   // 1000
2e6   // 2000000
0.1e2 // 10
```

#### `Number` object

Different built-in properties and functions are listed with their links, respectively [there](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Numbers_and_dates#Number_object).

#### `Math` object

Built-in properties: Math.PI
Built-in Functions: Math.floor(), Math.min(), etc. ([Information](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Numbers_and_dates#Math_object))

#### `Date` object

Create a new one:  

```js
var dateObjectName = new Date([parameters]);
```

Example 1:  

```js
var today = new Date();
var endYear = new Date(1995, 11, 31, 23, 59, 59, 999); // Set day and month
endYear.setFullYear(today.getFullYear()); // Set year to this year
var msPerDay = 24 * 60 * 60 * 1000; // Number of milliseconds per day
var daysLeft = (endYear.getTime() - today.getTime()) / msPerDay;
var daysLeft = Math.round(daysLeft); //returns days left in the year
```

Example 2:  

```js
function JSClock() {
  var time = new Date();
  var hour = time.getHours();
  var minute = time.getMinutes();
  var second = time.getSeconds();
  var temp = '' + ((hour > 12) ? hour - 12 : hour);
  if (hour == 0)
    temp = '12';
  temp += ((minute < 10) ? ':0' : ':') + minute;
  temp += ((second < 10) ? ':0' : ':') + second;
  temp += (hour >= 12) ? ' P.M.' : ' A.M.';
  return temp;
}
```

## Text Formatting

### Strings

#### String literals

Simple:

```js
'foo'
"bar"
```

Hexadecimal escape sequences:  

```js
'\xA9' // "©"
```

Unicode escape sequences:

```js
'\u00A9' // "©"
```

Unicode code point escapes:  

```js
'\u{2F804}'

// the same with simple Unicode escapes
'\uD87E\uDC04'
```

#### String Objects

```js
const foo = new String('foo'); // Creates a String object
console.log(foo); // Displays: [String: 'foo']
typeof foo; // Returns 'object'
const firstString = '2 + 2'; // Creates a string literal value
const secondString = new String('2 + 2'); // Creates a String object
eval(firstString); // Returns the number 4
eval(secondString); // Returns the string "2 + 2"
```

No need to create a String object, 'cause its [methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Text_formatting#Methods_of_String) could be called on String literals (js auto converts it to a String object and execute the methods, then discards that temporary object).

#### Multi-line template literals

##### Multi-lines

Traditional:  

```js
console.log('string text line 1\n\
string text line 2');
// "string text line 1
// string text line 2"
```

Now:  

```js
console.log(`string text line 1
string text line 2`);
// "string text line 1
// string text line 2"
```

##### Embedded expressions

```js
const five = 5;
const ten = 10;
console.log('Fifteen is ' + (five + ten) + ' and not ' + (2 * five + ten) + '.');
// "Fifteen is 15 and not 20."
```

### Internationalization

#### Date and time formatting

```js
const msPerDay = 24 * 60 * 60 * 1000;

// July 17, 2014 00:00:00 UTC.
const july172014 = new Date(msPerDay * (44 * 365 + 11 + 197));

const options = { year: '2-digit', month: '2-digit', day: '2-digit',
                hour: '2-digit', minute: '2-digit', timeZoneName: 'short' };
const americanDateTime = new Intl.DateTimeFormat('en-US', options).format;

console.log(americanDateTime(july172014)); // 07/16/14, 5:00 PM PDT
```

#### Number formatting

```
const gasPrice = new Intl.NumberFormat('en-US',
                        { style: 'currency', currency: 'USD',
                          minimumFractionDigits: 3 });

console.log(gasPrice.format(5.259)); // $5.259

const hanDecimalRMBInChina = new Intl.NumberFormat('zh-CN-u-nu-hanidec',
                        { style: 'currency', currency: 'CNY' });

console.log(hanDecimalRMBInChina.format(1314.25)); // ￥ 一,三一四.二五
```

#### Collation

The [Collator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Collator) object is useful for comparing and sorting strings.

```js
const names = ['Hochberg', 'Hönigswald', 'Holzman'];

const germanPhonebook = new Intl.Collator('de-DE-u-co-phonebk');

// as if sorting ["Hochberg", "Hoenigswald", "Holzman"]:
console.log(names.sort(germanPhonebook.compare).join(', '));
// logs "Hochberg, Hönigswald, Holzman"
```
```js
const germanDictionary = new Intl.Collator('de-DE-u-co-dict');

// as if sorting ["Hochberg", "Honigswald", "Holzman"]:
console.log(names.sort(germanDictionary.compare).join(', '));
// logs "Hochberg, Holzman, Hönigswald"
```

### Regular Expressions

* [Creating a regular expression](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions#Creating_a_regular_expression)
* [Special Chars](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions#Using_special_characters)

## Indexed collections

### Arrays

Similar to array I know.  
[Can be populated with own Property](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Indexed_collections#Populating_an_array).  
Has `forEach` function to [do a set function on each element](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach).   

### Typed Arrays

They have self descriptive names and provide views for all the usual numeric types like `Int8`, `Uint32`, `Float64` and so forth.

## Keyed collections

* [Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Keyed_collections#WeakSet_object)
* Map: Similar to dictionaries in python.
* Weakmap: Keys of WeakMaps are of the type Object only. Primitive data types as keys are not allowed (e.g. a Symbol can't be a WeakMap key). One difference to Map objects is that WeakMap keys are not enumerable (i.e., there is no method giving you a list of the keys). If they were, the list would depend on the state of garbage collection, introducing non-determinism.
* Set: A value in a Set may only occur once; it is unique in the Set's collection.
* Weakset: In contrast to Sets, WeakSets are collections of objects only and not of arbitrary values of any type. The WeakSet is weak: References to objects in the collection are held weakly. If there is no other reference to an object stored in the WeakSet, they can be garbage collected. That also means that there is no list of current objects stored in the collection. WeakSets are not enumerable.

[^1]: [Here Are 10 Projects You Can Do To Build Your JavaScript Skills](https://skillcrush.com/2018/06/18/projects-you-can-do-with-javascript/)
[^2]: [The homepage of the site](https://snorl.ax)
[^3]: [JavaScript Timing Events](https://www.w3schools.com/js/js_timing.asp)
[^4]: [JavaScript Guide - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
[^5]: [Template literals (Template strings) - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)
[^6]: [Notes on Types & Grammer (YDJS)](/terminal/2019/05/07/notes-on-types-grammer-ydjs/)
[^7]: [Promise - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
[^8]: [super - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/super)
