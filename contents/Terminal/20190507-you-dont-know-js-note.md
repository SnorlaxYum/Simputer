---
title: Notes on Types & Grammer (YDJS)
author: Sim
tags: js, You don't know Js, learning notes
status: published
summary: Notes on the first two chapters. I just started taking notes. Js is kinda confusing.
date: 2019-05-07 17:00
modified: 2019-05-17 22:24
Series: You Don't Know JS Read Note
---
Just started taking notes. Forgot to take notes on the former three. To summerize, js is about one object linked to another. A lot to learn for me. So it's best to learn it quickly the first time and then start learning by doing. I'll try Firebase function.  

## Chapter 1

In JavaScript, variables don't have types -- values have types. Variables can hold any value, at any time.

"not defined" means the var being not declared.
undefined means the var doesn't have a value.
undefined is our friend to check if the var has a value.
typeof returns undefined for both undeclared and undefined var

## Chapter 2

Array are also objects which can have keys/values.

String is an array consisting of immutable chars. Meanwhile array has lots of usable functions String don't have.
Use split to convert string to array then do the things.
Or use the array from the start.

Number:toFixed(digit) is similar to toPrecision(digit)
0.1+0.2 !== 0.3

We can use this Number.EPSILON to compare two numbers for "equality" (within the rounding error tolerance)

void: here's where don't understand, what's the use? I might look into it sometimes.

isNaN: 2 / "foo" etc

Infinity: 1/0

Object.is(a,b): Special Equality

## Chapter 3

They are constructors of type wrappers:

* `String()`
* `Number()`
* `Boolean()`
* `Array()`
* `Object()`
* `Function()`
* `RegExp()`
* `Date()`
* `Error()`
* `Symbol()` -- added in ES6!

For example, `var s = new String( "Hello World!" );` constructs a String wrapper. To convert it to String, `s.toString()`.  
Internal `[[class]]` can be inspected using `Object.prototype.toString.call()`.
Boxing wrapper is type wrapper having methods. Thankfully, JS will automatically box the primitive value to do methods. No need in doing things like `new String("abc")`, just use the primitive values like `"abc"`.  
Boolean wrapper created by `new boolean()` is truthy itself no matter it's true or false.
Use `valueof()` to unbox the warpper and get the value.

```js
var a = new String("abc");
a.valueof();
```

Unboxing can happen implicitly:  

```js
var a = new String( "abc" );
var b = a + ""; // `b` has the unboxed primitive value "abc"

typeof a; // "object"
typeof b; // "string"
```

Just as we've seen above with the other natives, these constructor forms should generally be avoided, unless you really know you need them, mostly because they introduce exceptions and gotchas that you probably don't really want to deal with.  

```js
var a = new Array( 3 );
var b = [ undefined, undefined, undefined ];
var c = [];
c.length = 3;

a;
b;
c;
```

```js
a.join( "-" ); // "--"
b.join( "-" ); // "--"

a.map(function(v,i){ return i; }); // [ undefined x 3 ]
b.map(function(v,i){ return i; }); // [ 0, 1, 2 ]
```

Bottom line: never ever, under any circumstances, should you intentionally create and use those empty-slot arrays. Just don't do it. They're nuts.

Also optional: Object(..), Function(..), and RegExp(..)  

The `Date(..)` and `Error(..)` native constructors are much more useful than the other natives, because there is no literal form for either. `Date.now()` shows a time value. `throw new Error("x wasn't provided")` throw a new error `"x wasn't provided"`. In addition to `Error()`, there are several specific-error-type natives though it's rare to use them manually: `EvalError(..)`, `RangeError(..)`, `ReferenceError(..)`, `SyntaxError(..)`, `TypeError(..)`, and `URIError(..)`.  

`Symbol` are unique in that you are not allowed to use `new` with it. Using them for private or special properties is likely their primary use-case. (Ex: `Symbol.ierator`, to define use `Symbol("statement")`)  

Some of the native Prototypes are aren't just plain objects:  

```js
typeof Function.prototype;			// "function"
Function.prototype();				// it's an empty function!

RegExp.prototype.toString();		// "/(?:)/" -- empty regex
"abc".match( RegExp.prototype );	// [""]
```

The chapter leads through a journey about knowing interestings underlying wrappers and prototypes. Hmm...... Hope to know something practical.  

## Chapter 4

Coercion is controversial. Most people run away from them. Try to get it more fully though it can be confusing.  

### Converting values

JavaScript coercions always result in one of the scalar primitive (see Chapter 2) values, like `string`, `number`, or `boolean`.  
In js, most people call all the types of conversions "coercion".
The author prefer to distinguish all the type conversion as "implicit coercion"(intended) vs. "explicit coercion."(occurred as a side effect of some other intentional operation)

__Example__:  

```js
var a = 42;

var b = a + "";			// implicit coercion

var c = String( a );	// explicit coercion
```

### Abstract Value Operations

#### `ToString`

The default `toString` (`StObject.prototype.toString()`) returns the *internal `[[Class]]`.  
If an object has its own `toString`, the result will be `string` instead.  

```js
var a = [1,2,3];

a.toString(); // "1,2,3"
```

##### JSON Stringification

Another task that seems awfully related to `ToString` is when you use the `JSON.stringify(..)` utility to serialize a value to a JSON-compatible `string` value.

```js
JSON.stringify( 42 );	// "42"
JSON.stringify( "42" );	// ""42"" (a string with a quoted string value in it)
JSON.stringify( null );	// "null"
JSON.stringify( true );	// "true"
```

`JSON.stringify(..)` with an `object` as argument can make an error thrown.  

```js
var o = { };

var a = {
	b: 42,
	c: o,
	d: function(){}
};

// create a circular reference inside `a`
o.e = a;

// would throw an error on the circular reference
// JSON.stringify( a );

// define a custom JSON value serialization
a.toJSON = function() {
	// only include the `b` property for serialization
	return { b: this.b };
};

JSON.stringify( a ); // "{"b":42}"
```
`toJSON()` should be interpreted as "to a JSON-safe value suitable for stringification," not "to a JSON string" as many developers mistakenly assume.

```js
var a = {
	val: [1,2,3],

	// probably correct!
	toJSON: function(){
		return this.val.slice( 1 );
	}
};

var b = {
	val: [1,2,3],

	// probably incorrect!
	toJSON: function(){
		return "[" +
			this.val.slice( 1 ).join() +
		"]";
	}
};

JSON.stringify( a ); // "[2,3]"

JSON.stringify( b ); // ""[2,3]""
```

Lesser known functionality:
__replacer__: An optional second argument can be passed to `JSON.stringify(..)`. Can be an `array` or a `function`.  

```js
var a = {
	b: 42,
	c: "42",
	d: [1,2,3]
};

JSON.stringify( a, ["b","c"] ); // "{"b":42,"c":"42"}"

JSON.stringify( a, function(k,v){
	if (k !== "c") return v;
} );
// "{"b":42,"d":[1,2,3]}"
```

`space`: A third argument passed to `JSON.stringify(..)`. Can be a positive number (how many space characters shoule be used at each indentation level) or a `string` (up to the first ten characters of its value will be used for each indentation level).  

```js
var a = {
	b: 42,
	c: "42",
	d: [1,2,3]
};

JSON.stringify( a, null, 3 );
// "{
//    "b": 42,
//    "c": "42",
//    "d": [
//       1,
//       2,
//       3
//    ]
// }"

JSON.stringify( a, null, "-----" );
// "{
// -----"b": 42,
// -----"c": "42",
// -----"d": [
// ----------1,
// ----------2,
// ----------3
// -----]
// }"
```

1. `string`, `number`, `boolean`, and `null` values all stringify for JSON basically the same as how they coerce to `string` values via the rules of the `ToString` abstract operation.
2. If you pass an `object` value to `JSON.stringify(..)`, and that `object` has a `toJSON()` method on it, `toJSON()` is automatically called to (sort of) "coerce" the value to be *JSON-safe* before stringification.

#### `toNumber`

Convert a non-`number` value to a `number`. If the conversion fails, it will return a `NaN` instead.  

```js
var a = {
	valueOf: function(){
		return "42";
	}
};

var b = {
	toString: function(){
		return "42";
	}
};

var c = [4,2];
c.toString = function(){
	return this.join( "" );	// "42"
};

Number( a );			// 42
Number( b );			// 42
Number( c );			// 42
Number( "" );			// 0
Number( [] );			// 0
Number( [ "abc" ] );	// NaN
```

#### `toBoolean`

One thing to notice: `0` can be coerced to `false`, or `1` to `true` (and vice versa). But they r not the same.

##### Falsy Values

So-called falsy values will be coerced into `false` if you force a `boolean` coercion on it:

* `undefined`
* `null`
* `false`
* `+0`, `-0`, and `NaN`
* `""`

##### Falsy Objects

As the name says, they r objects ... `false` .... `boolean` coercion ....  

```js
var a = new Boolean( false );
var b = new Number( 0 );
var c = new String( "" );
```

THey seem to be falsy, but that's not true:  

```js
var a = new Boolean(false);
var b = new Boolean(0);
var c = new Boolean("");
a && b && c;
// Boolean { false }
a;
// Boolean { false }
var d = Boolean(a && b && c);
d;
// true
var d = a && b && c;
d;
// Boolean { false }
b;
// Boolean { false }
c;
// Boolean { false }
Boolean(a);
// true
Boolean(b);
// true
Boolean(c);
// true

```

A most well-known case:  

```js
Boolean(document.all);
// false
```

`document.all` itself was never really "standard" and has long since been deprecated/abandoned. They are used as a means of detecting old, nonstandard IE.  

##### Truthy Values

It's the counterpart of the falsy values.  

My runs for the examples:  

```js
var a = "false";
var b = "0";
var c = "''";
var d = Boolean(a && b && c);
d;
// true
a;
// "false"
b;
// "0"
c;
// "''"
a && b && c;
// "''"
var a = [];
var b = {};
var c = function(){};
var d = Boolean(a && b && c);
d;
// true
```

To know whether a value is truthy, consult a finite falsy list. A truthy list would be infinitely long.  

### Explicit Coercion

As the name says, the coercion is explicit and obvious.  

#### Strings <==> Numbers

Don't use the `new` keyword as in doing such a wrapped object will be created.  
My runs:  

```js
var a = 42;
var b = String(a);
var c = "3.14";
var d = Number(c);
b;
// "42"
d;
// 3.14
```

My runs on another way:  

```js
//inherited from previously created var a, c
var b = a.toString();
var d = +c;
b;
// "42"
d;
// 3.14
```

Something implicit happened here: `a` was automatically boxed as the primitive value doesn't have the function.  
THe unary `+` is explicitly intended for `number` coercion.  

`++` and `--` have the side effect like they do in c/c++.  

```js
var c = "3.14";
var d = 5 + -c;
d;
// 1.8599999999999999
var d = 5 + +c;
d;
// 8.14
var d = 5 + ++c;
d;
// 9.14
var d = 5 + --c;
d;
// 8.14
c;
// 3.1400000000000006
var d = 5 + --c;
c;
// 2.1400000000000006
```

Trying to be explicit and __reduce confusion__, not make it worse.  

##### `Date` To `Number`

Use `+` to coerce a date into a `number` that is the unix timestamp.  

```js
var d = new Date("2019-05-09 20:00");

+d;
// 1557403200000
```

`+` get the now moment as a timestamp:  

```js
var now_timestamp = +new Date();
now_timestamp;
// 1557403504691
```

Due to a peculiar syntactic "trick", it's doable to omit `()`:  

```js
var now_timestamp = +new Date;
now_timestamp;
// 1557403628543
```

A noncoercion approach is preferred:  

```js
var timestamp = new Date().getTime();
timestamp
// 1557405924752
```

A more prefferred and recommended way:  

```js
var timestamp = Date.now();

timestamp;
// 1557406018081
```

##### The Curious Case of the `~`

It's a bitwise operator.  

It's pretty common to try to use `indexOf(..)` not just as an operation to get the position, but as a `boolean` check of presence/absence of a substring in another `string`. Here's how developers usually perform such checks:

```js
var a = "Hello world";
if (a.indexOf("lo") >= 0) {
  console.log("True hmm.......");
}
// True hmm.......
if (a.indexOf("lo") != -1) {
  console.log("Uh");
}
// Uh
if (a.indexOf("ol") < 0) {
  console.log("Uh");
}
// Uh
if (a.indexOf("ol") == -1) {
  console.log("Uh");
}
// Uh
a.indexOf("lo")
// 3
a.indexOf("ol")
// -1
```

Whether the substring is found or not, the number is treated as true in `if`.  

```js
~a.indexOf("lo");
// -4
if (~a.indexOf("lo")) {
  console.log("Found 'lo'");
}
// Found 'lo'
~a.indexOf("ol");
// 0
!~a.indexOf("ol");
// true
!~a.indexOf("lo");
// false
if (!~a.indexOf("ol")) {
  console.log("Not found");
}
// Not found
if (a.indexOf("ol")) {
  console.log("Found");
}
// no output
```

`~` takes the return value of `indexOf(..)` and transforms it: for the "failure" `-1` we get the falsy `0`, and every other value is truthy.

###### Truncating Bits

`~~` to truncate the decimal part of a `number`. First, it only works reliably on 32-bit values. But more importantly, it doesn't work the same on negative numbers as `Math.floor(..)` does:  

```js
Math.floor(-49.6);
// -50
~~-49.6;
// -49
```

`x | 0` does the same job, but:  

```JS
~~1E20 /10;
// 166199296
~~1E20 | 0 /10;
// 1661992960
(~~1E20 | 0) /10;
// 166199296
```
#### Explicitly: Parsing Numeric Strings

Between parsing and type conversion:  

```js
var a = "42";
var b = "42px";
Number(a);
// 42
Number(b);
// NaN
parseInt(a);
// 42
parseInt(b);
// 42
```

a twin of `parseInt`: `parseFloat`

In `parseInt`, it's safe to pass the second parameter to set the base:  

```js
var min = parseInt("09");
var hour = parseInt("08");
min;
// 9
hour;
// 8
var hour = parseInt("08", 8);
hour;
// 0
var hour = parseInt("09", 8);
hour;
// 0
```

##### Parsing Non-Strings

All output are predictable in that all `js` representation have some sort of default `string` representation:  

```js
parseInt(1/0, 18);
// NaN
parseInt(new String("42"));
// 42
var a = {
    num: 21,
    toString: function() { return String( this.num * 2 ); }
};
parseInt( a );
// 42
parseInt(0.000008);
// 0
parseInt(0.0000008);
// 8
parseInt(false, 16);
// 250
parseInt(parseInt, 16);
// 15
parseInt("0x10");
// 16
parseInt("103", 2);
// 2
```

#### Explicitly: * --> Boolean

This is not recommended in js:  

```js
var a = 42;

var b = a ? true : false;
```
`a` should be coerced to `boolean` first.

`Boolean(a)` and `!!a` are far better as *explicit* coercion options.

```js

var a = "0";
var b = [];
var b = {};
var c = [];
var d = "";
var e = 0;
var f = null;
var g;
Boolean(a);
// true
Boolean(b);
// true
Boolean(c);
// true
Boolean(d);
// false
Boolean(e);
// false
Boolean(f);
// false
Boolean(g);
// false
!!a;
// true
!!b;
// true
!!c;
// true
!!d;
// false
!!e;
// false
!!f;
// false
!!g;
// false
var a = [
    1,
    function(){ /*..*/ },
    2,
    function(){ /*..*/ }
];
JSON.stringify( a );
// "[1,null,2,null]"
JSON.stringify( a, function(key,val){
    if (typeof val == "function") {
        // force `ToBoolean` coercion of the function
        return !!val;
    }
    else {
        return val;
    }
} );
// "[1,true,2,true]"
```

### Implicit Coercion

#### Simplifying Implicitly

There are good part in "implicit", don't refuse it. I guess that what it talks about.  

#### Implicitly: Strings <==> Numbers

Common concatenation:  

```js
var a = "42";
var b = "0";

var c = 42;
var d = 0;

a + b; // "420"
c + d; // 42
```

Array turned into string:  

```js
var a = [1,2];
var b = [3,4];

a + b; // "1,23,4"
```

According to ES5 spec section 11.6.1, the `+` algorithm (when an `object` value is an operand) will concatenate if either operand is either already a `string`, or if the following steps produce a `string` representation. So, when `+` receives an `object` (including `array`) for either operand, it first calls the `ToPrimitive` abstract operation (section 9.1) on the value, which then calls the `[[DefaultValue]]` algorithm (section 8.12.8) with a context hint of `number`.  

Coerce a number to a string:  

```js
var a = 42;
var b = a + "";

b; // "42"
```

If you're using an `object` instead of a regular primitive `number` value, you may not necessarily get the *same* `string` value!

Consider:  

```js
var a = {
	valueOf: function() { return 42; },
	toString: function() { return 4; }
};

a + "";			// "42"

String( a );	// "4"
```

Implicitly coerce* from `string` to `number`:  

```js
var a = "3.14";
var b = a - 0;

b; // 3.14
```

The `-` operator is defined only for numeric subtraction, so `a - 0` forces `a`'s value to be coerced to a `number`. While far less common, `a * 1` or `a / 1` would accomplish the same result, as those operators are also only defined for numeric operations.  

Object value with `-`:  

```js
var a = [3];
var b = [1];

a - b; // 2
```

#### Implicitly: Booleans --> Numbers

```js
function onlyOne(a,b,c) {
  return !!((a && !b && !c) ||
            (!a && b && !c) || (!a && !b && c));
}
var a = true;
var b = false;
onlyOne(a,b,b);
// true
onlyOne(b,b,b);
// false
```

If there are four or more to get only one true:  

```js
function onlyOne() {
	var sum = 0;
	for (var i=0; i < arguments.length; i++) {
		// skip falsy values. same as treating
		// them as 0's, but avoids NaN's.
		if (arguments[i]) {
			sum += arguments[i];
		}
	}
	return sum == 1;
}

var a = true;
var b = false;

onlyOne( b, a );		// true
onlyOne( b, a, b, b, b );	// true

onlyOne( b, b );		// false
onlyOne( b, a, b, b, b, a );	// false
```

A version using `reduce(..)`[^1]:  

```js
function onlyOne() {
  return Object.values(arguments).reduce((total, current) => total + current) == 1;
}
onlyOne(a,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,a);
// false
onlyOne(a,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b);
// true
```

[^1]: [Array.prototype.reduce() - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)

Explicit version:  

```js
function onlyOne() {
	var sum = 0;
	for (var i=0; i < arguments.length; i++) {
		sum += Number( !!arguments[i] );
	}
	return sum === 1;
}
```

#### Implicitly: * --> Boolean

```js
var a = 42;
var b = "abc";
var c;
var d = null;

if (a) {
	console.log( "yep" );		// yep
}

while (c) {
	console.log( "nope, never runs" );
}

c = d ? a : b;
c;					// "abc"

if ((a && d) || c) {
	console.log( "yep" );		// yep
}
```

#### Operators `||` and `&&`


Quoting the ES5 spec from section 11.11:

> The value produced by a && or || operator is not necessarily of type Boolean. The value produced will always be the value of one of the two operand expressions.


```js
var a = 42;
var b = "abc";
var c = null;

a || b;		// 42
a && b;		// "abc"

c || b;		// "abc"
c && b;		// null
```

Both operators will always test the first operands.

Below, "RES" == "The result of the first operands".  

|  RES\Operand   |      `||`      |      `&&`      |
| :------------- | :------------- | :------------- |
| `true`         | The first      | The second     |
| `false`        | The second     | The first      |

The table tells that what will be returned from the operator in certain condition.  

#### Symbol Coercion

```js
var s1 = Symbol( "cool" );
String( s1 );					// "Symbol(cool)"

var s2 = Symbol( "not cool" );
s2 + "";						// TypeError
```

The good news: it's probably going to be exceedingly rare for you to need to coerce a `symbol` value. The way they're typically used (see Chapter 3) will probably not call for coercion on a normal basis.

### Loose Equals vs. Strict Equals

Loose equals is the `==` operator, and strict equals is the `===` operator. Both operators are used for comparing two values for "equality," but the "loose" vs. "strict" indicates a **very important** difference in behavior between the two, specifically in how they decide "equality."  

A very common misconception about these two operators is: "`==` checks values for equality and `===` checks both values and types for equality."  

The correct description is: "`==` allows coercion in the equality comparison and `===` disallows coercion."

#### Equality Performance

If you want coercion, use `==` loose equality, but if you don't want coercion, use `===` strict equality.

**Note:** The implication here then is that both `==` and `===` check the types of their operands. The difference is in how they respond if the types don't match.

#### Abstract Equality

Basically, the first clause (11.9.3.1) says, if the two values being compared are of the same type, they are simply and naturally compared via Identity as you'd expect. For example, `42` is only equal to `42`, and `"abc"` is only equal to `"abc"`.

Some minor exceptions to normal expectation to be aware of:

* `NaN` is never equal to itself (see Chapter 2)
* `+0` and `-0` are equal to each other (see Chapter 2)

The final provision in clause 11.9.3.1 is for `==` loose equality comparison with `object`s (including `function`s and `array`s). Two such values are only *equal* if they are both references to *the exact same value*. No coercion occurs here.

**Note:** The `===` strict equality comparison is defined identically to 11.9.3.1, including the provision about two `object` values. It's a very little known fact that **`==` and `===` behave identically** in the case where two `object`s are being compared!

The rest of the algorithm in 11.9.3 specifies that if you use `==` loose equality to compare two values of different types, one or both of the values will need to be *implicitly* coerced. This coercion happens so that both values eventually end up as the same type, which can then directly be compared for equality using simple value Identity.

**Note:** The `!=` loose not-equality operation is defined exactly as you'd expect, in that it's literally the `==` operation comparison performed in its entirety, then the negation of the result. The same goes for the `!==` strict not-equality operation.

##### Comparing: `string`s to `number`s

```js
var a = 42;
var b = "42";

a === b;	// false
a == b;		// true
```
In the ES5 spec, clauses 11.9.3.4-5 say:

> 4. If Type(x) is Number and Type(y) is String,
>    return the result of the comparison x == ToNumber(y).
> 5. If Type(x) is String and Type(y) is Number,
>    return the result of the comparison ToNumber(x) == y.

According to this, it's the string `"42"` coerced into the number `42` when the `==` is used.

##### Comparing: anything to `boolean`

```js
var a = "42";
var b = true;

a == b;	// false
```

Let's again quote the spec, clauses 11.9.3.6-7:

> 6. If Type(x) is Boolean,
>    return the result of the comparison ToNumber(x) == y.
> 7. If Type(y) is Boolean,
>    return the result of the comparison x == ToNumber(y).

It's __not performing a boolean test__. The boolean was just coerced into number `1`.  

```js
var a = "42";

// bad (will fail!):
if (a == true) {
	// ..
}

// also bad (will fail!):
if (a === true) {
	// ..
}

// good enough (works implicitly):
if (a) {
	// ..
}

// better (works explicitly):
if (!!a) {
	// ..
}

// also great (works explicitly):
if (Boolean( a )) {
	// ..
}
```

##### Comparing: `null`s to `undefined`s

Another example of *implicit* coercion can be seen with `==` loose equality between `null` and `undefined` values. Yet again quoting the ES5 spec, clauses 11.9.3.2-3:

> 2. If x is null and y is undefined, return true.
> 3. If x is undefined and y is null, return true.

```js
var a = null;
var b;

a == b;		// true
a == null;	// true
b == null;	// true

a == false;	// false
b == false;	// false
a == "";	// false
b == "";	// false
a == 0;		// false
b == 0;		// false
```

The author recommends using this coercion to allow `null` and `undefined` to be indistinguishable and thus treated as the same value.


For example:

```js
var a = doSomething();

if (a == null) {
	// ..
}
```

The `a == null` only pass when a is either `null` or `undefined`  

THe uglier explicit version:  

```js
var a = doSomething();

if (a === undefined || a === null) {
	// ..
}
```

It's reliable safe way of using implicit coersion.  

##### Comparing: `object`s to non-`object`s

If an `object`/`function`/`array` is compared to a simple scalar primitive (`string`, `number`, or `boolean`), the ES5 spec says in clauses 11.9.3.8-9:

> 8. If Type(x) is either String or Number and Type(y) is Object,
>    return the result of the comparison x == ToPrimitive(y).
> 9. If Type(x) is Object and Type(y) is either String or Number,
>    return the result of the comparison ToPrimitive(x) == y.

No boolean 'cause in a `==` sentence a boolean will always be coerced into a `Number` first.  

There are some values where this is not the case, though, because of other overriding rules in the `==` algorithm. Consider:

```js
var a = null;
var b = Object( a );	// same as `Object()`
a == b;					// false

var c = undefined;
var d = Object( c );	// same as `Object()`
c == d;					// false

var e = NaN;
var f = Object( e );	// same as `new Number( e )`
e == f;					// false
```

The `null` and `undefined` values cannot be boxed -- they have no object wrapper equivalent -- so `Object(null)` is just like `Object()` in that both just produce a normal object.

`NaN` can be boxed to its `Number` object wrapper equivalent, but when `==` causes an unboxing, the `NaN == NaN` comparison fails because `NaN` is never equal to itself (see Chapter 2).  

#### Edge Cases

This section the worst, craziest corner cases will be called so we can see what we need to avoid to not get bitten with coercion bugs.

##### A Number By Any Other Value Would...

```js
Number.prototype.valueOf = function() {
	return 3;
};

new Number( 2 ) == 3;	// true
```

It's trap that should be avoided.  


```js
var i = 2;

Number.prototype.valueOf = function() {
	return i++;
};

var a = new Number( 42 );

if (a == 2 && a == 3) {
	console.log( "Yep, this happened." );
}
// Yep, this happened.
```

Avoid these crazy tricks, and stick only with valid and proper usage of coercion.

##### False-y Comparisons

```js
"0" == null;			// false
"0" == undefined;		// false
"0" == false;			// true -- UH OH!
"0" == NaN;				// false
"0" == 0;				// true
"0" == "";				// false

false == null;			// false
false == undefined;		// false
false == NaN;			// false
false == 0;				// true -- UH OH!
false == "";			// true -- UH OH!
false == [];			// true -- UH OH!
false == {};			// false

"" == null;				// false
"" == undefined;		// false
"" == NaN;				// false
"" == 0;				// true -- UH OH!
"" == [];				// true -- UH OH!
"" == {};				// false

0 == null;				// false
0 == undefined;			// false
0 == NaN;				// false
0 == [];				// true -- UH OH!
0 == {};				// false
```

`UH OH!` comparisons are false positives.  

```js
[] == ![];		// true
```

```js
2 == [2];		// true
"" == [null];	// true
```

```js
0 == "\n";		// true
```


To contrast against these 24 likely suspects for coercion gotchas, consider another list like this:

```js
42 == "43";							// false
"foo" == 42;						// false
"true" == true;						// false

42 == "42";							// true
"foo" == [ "foo" ];					// true
```

In these nonfalsy, noncorner cases (and there are literally an infinite number of comparisons we could put on this list), the coercion results are totally safe, reasonable, and explainable.

#### Sanity Check

Avoid list in coercion:  

```js
"0" == false;			// true -- UH OH!
false == 0;				// true -- UH OH!
false == "";			// true -- UH OH!
false == [];			// true -- UH OH!
"" == 0;				// true -- UH OH!
"" == [];				// true -- UH OH!
0 == [];				// true -- UH OH!
```

Boolean in `==` should be avoided. And it was mentioned before. So the list is down to three:  

```js
"" == 0;				// true -- UH OH!
"" == [];				// true -- UH OH!
0 == [];				// true -- UH OH!
```

##### Safely Using Implicit Coercion

Some heuristic rules to follow:

1. If either side of the comparison can have `true` or `false` values, don't ever, EVER use `==`.
2. If either side of the comparison can have `[]`, `""`, or `0` values, seriously consider not using `==`.

**Being more explicit/verbose in these cases will save you from a lot of headaches.**

### Abstract Relational Comparison

```js
var a = [ 42 ];
var b = [ "43" ];

a < b;	// true
b < a;	// false
```

Similar to `==`  

```js
var a = [ "42" ];
var b = [ "043" ];

a < b;	// false
```

`a` and `b` are *not* coerced to `number`s, because both of them end up as `string`s after the `ToPrimitive` coercion on the two `array`s. So, `"42"` is compared character by character to `"043"`, starting with the first characters `"4"` and `"0"`, respectively. Since `"0"` is lexicographically *less than* than `"4"`, the comparison returns `false`.


```js
var a = { b: 42 };
var b = { b: 43 };

a < b;	// ??
```

`a < b` is also `false`, because `a` becomes `[object Object]` and `b` becomes `[object Object]`, and so clearly `a` is not lexicographically less than `b`.  

Strange:  

```js
var a = { b: 42 };
var b = { b: 43 };

a < b;	// false
a == b;	// false
a > b;	// false

a <= b;	// true
a >= b;	// true
```

`a <= b` is just the opposite result of `a < b`  

If coercion is helpful and reasonably safe, like in a `42 < "43"` comparison, **use it**. On the other hand, if you need to be safe about a relational comparison, *explicitly coerce* the values first, before using `<` (or its counterparts).

```js
var a = [ 42 ];
var b = "043";

a < b;						// false -- string comparison!
Number( a ) < Number( b );	// true -- number comparison!
```

## Chapter 5

Talking about js' grammer.

### Statements & Expressions

```js
var a = 3 * 6;
var b = a;
b;
```

Expressions: `3 * 6` on the first line, `a` on the second line.  
Statements: each of the three lines.

#### Statement Completion Values

`var`'s completion value is empty (`undefined`) due to the value swallowed up.  

`undefined` is quite common as completion values.  

```js
var b;

if (true) {
	b = 4 + 38;
}
```

This returns 42. In other words, the completion value of a block is like an *implicit return* of the last statement value in the block.

To catch the completion value: (Only demo, don't do it. `eval(..)` sometimes pronounced "evil")  

```js
var a, b;

a = eval( "if (true) { b = 4 + 38; }" );

a;	// 42
```

There's a proposal for ES7 called "do expression." Here's how it might work:

```js
var a, b;

a = do {
	if (true) {
		b = 4 + 38;
	}
};

a;	// 42
```

#### Expression Side Effects

```js
function foo() {
	a = a + 1;
}

var a = 1;
foo();		// result: `undefined`, side effect: changed `a`
```

```js
var a = 42;
var b = a++;

a;	// 43
b;	// 42
```

THe same behaviour in C code:  


```js
var a = 42;

a++;	// 42
a;		// 43

++a;	// 44
a;		// 44
```

The expression `a++` has two separate behaviors. *First*, it returns the current value of `a`, which is `42` (which then gets assigned to `b`). But *next*, it changes the value of `a` itself, incrementing it by one.

```js
var a = 42, b;
b = ( a++, a );

a;	// 43
b;	// 43
```

**Note:** The `( .. )` around `a++, a` is required here. The reason is operator precedence, which we'll cover later in this chapter.

```js
var obj = {
	a: 42
};

obj.a;			// 42
delete obj.a;	// true
obj.a;			// undefined
```

The result value of the `delete` operator is `true` if the requested operation is valid/allowable, or `false` otherwise. But the side effect of the operator is that it removes the property (or array slot).  

```js
var a;

a = 42;		// 42
a;			// 42
```

It may not seem like `=` in `a = 42` is a side-effecting operator for the expression. But if we examine the result value of the `a = 42` statement, it's the value that was just assigned (`42`), so the assignment of that same value into `a` is essentially a side effect.  


```js
var a, b, c;

a = b = c = 42;
```

Here, `c = 42` is evaluated to `42` (with the side effect of assigning `42` to `c`), then `b = 42` is evaluated to `42` (with the side effect of assigning `42` to `b`), and finally `a = 42` is evaluated (with the side effect of assigning `42` to `a`).  

Another scenario to consider:

```js
function vowels(str) {
	var matches;

	if (str) {
		// pull out all the vowels
		matches = str.match( /[aeiou]/g );

		if (matches) {
			return matches;
		}
	}
}

vowels( "Hello World" ); // ["e","o","o"]
```

This works, and many developers prefer such. But using an idiom where we take advantage of the assignment side effect, we can simplify by combining the two `if` statements into one:

```js
function vowels(str) {
	var matches;

	// pull out all the vowels
	if (str && (matches = str.match( /[aeiou]/g ))) {
		return matches;
	}
}

vowels( "Hello World" ); // ["e","o","o"]
```

**Note:** The `( .. )` around `matches = str.match..` is required. The reason is operator precedence, which we'll cover in the "Operator Precedence" section later in this chapter.

I prefer this shorter style, as I think it makes it clearer that the two conditionals are in fact related rather than separate. But as with most stylistic choices in JS, it's purely opinion which one is *better*.  

#### Contextual Rules

##### `{ .. }` Curly Braces

###### Object Literals

```js
// assume there's a `bar()` function defined

var a = {
	foo: bar()
};
```

How do we know this is an `object` literal? Because the `{ .. }` pair is a value that's getting assigned to `a`.  

###### Labels

JS *does* support a limited, special form of `goto`: labeled jumps.  

```js
// `foo` labeled-loop
foo: for (var i=0; i<4; i++) {
	for (var j=0; j<4; j++) {
		// whenever the loops meet, continue outer loop
		if (j == i) {
			// jump to the next iteration of
			// the `foo` labeled-loop
			continue foo;
		}

		// skip odd multiples
		if ((j * i) % 2 == 1) {
			// normal (non-labeled) `continue` of inner loop
			continue;
		}

		console.log( i, j );
	}
}
// 1 0
// 2 0
// 2 1
// 3 0
// 3 2
```

The use of `break`:  

```js
// `foo` labeled-loop
foo: for (var i=0; i<4; i++) {
	for (var j=0; j<4; j++) {
		if ((i * j) >= 3) {
			console.log( "stopping!", i, j );
			// break out of the `foo` labeled loop
			break foo;
		}

		console.log( i, j );
	}
}
// 0 0
// 0 1
// 0 2
// 0 3
// 1 0
// 1 1
// 1 2
// stopping! 1 3
```

###### Blocks

```js
[] + {}; // "[object Object]"
{} + []; // 0
```

###### Object Destructuring

Starting with ES6, another place that you'll see `{ .. }` pairs showing up is with "destructuring assignments" (see the *ES6 & Beyond* title of this series for more info), specifically `object` destructuring. Consider:

```js
function getData() {
	// ..
	return {
		a: 42,
		b: "foo"
	};
}

var { a, b } = getData();

console.log( a, b ); // 42 "foo"
```

Object destructuring with a `{ .. }` pair can also be used for named function arguments, which is sugar for this same sort of implicit object property assignment:

```js
function foo({ a, b, c }) {
	// no need for:
	// var a = obj.a, b = obj.b, c = obj.c
	console.log( a, b, c );
}

foo( {
	c: [1,2,3],
	a: 42,
	b: "foo"
} );	// 42 "foo" [1, 2, 3]
```

##### `else if` And Optional Blocks


It's a common misconception that JavaScript has an `else if` clause, because you can do:

```js
if (a) {
	// ..
}
else if (b) {
	// ..
}
else {
	// ..
}
```

But there's a hidden characteristic of the JS grammar here: there is no `else if`. But `if` and `else` statements are allowed to omit the `{ }` around their attached block if they only contain a single statement. You've seen this many times before, undoubtedly:

```js
if (a) doSomething( a );
```

However, the exact same grammar rule applies to the `else` clause, so the `else if` form you've likely always coded is *actually* parsed as:

```js
if (a) {
	// ..
}
else {
	if (b) {
		// ..
	}
	else {
		// ..
	}
}
```

Recall the example from above:

```js
var a = 42, b;
b = ( a++, a );

a;	// 43
b;	// 43
```

But what would happen if we remove the `( )`?

```js
var a = 42, b;
b = a++, a;

a;	// 43
b;	// 42
```

Because the `,` operator has a lower precedence than the `=` operator.  

Now, recall this example from above:

```js
if (str && (matches = str.match( /[aeiou]/g ))) {
	// ..
}
```

We said the `( )` around the assignment is required, but why? Because `&&` has higher precedence than `=`, so without the `( )` to force the binding, the expression would instead be treated as `(str && matches) = str.match..`. But this would be an error, because the result of `(str && matches)` isn't going to be a variable, but instead a value (in this case `undefined`), and so it can't be the left-hand side of an `=` assignment!  

#### Short Circuited


This short circuiting can be very helpful and is commonly used:

```js
function doSomething(opts) {
	if (opts && opts.cool) {
		// ..
	}
}
```

Similarly, you can use `||` short circuiting:

```js
function doSomething(opts) {
	if (opts.cache || primeCache()) {
		// ..
	}
}
```

#### Tighter Binding

```js
a && b || c ? c || b ? a : c && b : a
```

Is that more like this:

```js
a && b || (c ? c || (b ? a : c) && b : a)
```

or this?

```js
(a && b || c) ? (c || b) ? a : (c && b) : a
```

The answer is the second one. But why?

__Because `&&` is more precedent than `||`, and `||` is more precedent than `? :`.__ (`&&` > `||` > `||`)  

#### Associativity

In general, operators are either left-associative or right-associative, referring to whether **grouping happens from the left or from the right**.  

Technically, `a && b && c` will be handled as `(a && b) && c`, because `&&` is left-associative (so is `||`, by the way). However, the right-associative alternative `a && (b && c)` behaves observably the same way. For the same values, the same expressions are evaluated in the same order.  

So it doesn't really matter that much that `&&` and `||` are left-associative, other than to be accurate in how we discuss their definitions.  

But that's not always the case. Some operators would behave very differently depending on left-associativity vs. right-associativity.  

The `? :` ("ternary" or "conditional") operator is right-associative:

```js
a ? b : c ? d : e;
```

#### Disambiguation

**use operator precedence/associativity where it leads to shorter and cleaner code, but use `( )` manual grouping in places where it helps create clarity and reduce confusion.**

### Automatic Semicolons

JS won't treat `c` as the next line as part of the `var` statement if no `,` is between `b` and `c`:  

```js
var a = 42, b
c;
```

Similar:  

```js
var a = 42, b = "foo";

a
b	// "foo"
```

Where ASI is helpful:  

```js
var a = 42;

do {
	// ..
} while (a)	// <-- ; expected here!
a;
```

Statement blocks do not require `;` termination, so ASI isn't necessary:

```js
var a = 42;

while (a) {
	// ..
} // <-- no ; expected here
a;
```

The other major case where ASI kicks in is with the `break`, `continue`, `return`, and (ES6) `yield` keywords:

```js
function foo(a) {
	if (!a) return
	a *= 2;
	// ..
}
```

The `return` statement doesn't carry across the newline to the `a *= 2` expression, as ASI assumes the `;` terminating the `return` statement. Of course, `return` statements *can* easily break across multiple lines, just not when there's nothing after `return` but the newline/line break.

```js
function foo(a) {
	return (
		a * 2 + 3 / 12
	);
}
```

Identical reasoning applies to `break`, `continue`, and `yield`.

#### Error Correction

The author: **use semicolons wherever you know they are "required," and limit your assumptions about ASI to a minimum.**

But don't just take my word for it. Back in 2012, creator of JavaScript Brendan Eich said (http://brendaneich.com/2012/04/the-infernal-semicolon/) the following:

> The moral of this story: ASI is (formally speaking) a syntactic error correction procedure. If you start to code as if it were a universal significant-newline rule, you will get into trouble.
> ..
> I wish I had made newlines more significant in JS back in those ten days in May, 1995.
> ..
> Be careful not to use ASI as if it gave JS significant newlines.

### Errors

Invalid syntax:  

```js
var a = /+foo/;		// Error!
```

The wrong target of an assignment:  

```js
var a;
42 = a;		// Error!
```

ES5's `strict` mode defines even more early errors. For example, in `strict` mode, function parameter names cannot be duplicated:

```js
function foo(a,b,a) { }					// just fine

function bar(a,b,a) { "use strict"; }	// Error!
```

Another `strict` mode early error is an object literal having more than one property of the same name:

```js
(function(){
	"use strict";

	var a = {
		b: 42,
		b: 43
	};			// Error!
})();
```

#### Using Variables Too Early

ES6 defines a (frankly confusingly named) new concept called the TDZ ("Temporal Dead Zone").

The TDZ refers to places in code where a variable reference cannot yet be made, because it hasn't reached its required initialization.  


```js
{
	a = 2;		// ReferenceError!
	let a;
}
```

The assignment `a = 2` is accessing the `a` variable (which is indeed block-scoped to the `{ .. }` block) before it's been initialized by the `let a` declaration, so it's in the TDZ for `a` and throws an error.  

Interestingly, while `typeof` has an exception to be safe for undeclared variables (see Chapter 1), no such safety exception is made for TDZ references:

```js
{
	typeof a;	// undefined
	typeof b;	// ReferenceError! (TDZ)
	let b;
}
```

### Function Arguments

Another example of a TDZ violation can be seen with ES6 default parameter values (see the *ES6 & Beyond* title of this series):

```js
var b = 3;

function foo( a = 42, b = a + b + 5 ) {
	// ..
}
```

The `b` reference in the assignment would happen in the TDZ for the parameter `b` (not pull in the outer `b` reference), so it will throw an error. However, the `a` in the assignment is fine since by that time it's past the TDZ for parameter `a`.

When using ES6's default parameter values, the default value is applied to the parameter if you either omit an argument, or you pass an `undefined` value in its place:

```js
function foo( a = 42, b = a + 1 ) {
	console.log( a, b );
}

foo();					// 42 43
foo( undefined );		// 42 43
foo( 5 );				// 5 6
foo( void 0, 7 );		// 42 7
foo( null );			// null 1
```

**Note:** `null` is coerced to a `0` value in the `a + 1` expression. See Chapter 4 for more info.  

Even though the default parameter values are applied to the `a` and `b` parameters, if no arguments were passed in those slots, the `arguments` array will not have entries:  

```js
function foo( a = 42, b = a + 1 ) {
	console.log(
		arguments.length, a, b,
		arguments[0], arguments[1]
	);
}

foo();					// 0 42 43 undefined undefined
foo( 10 );				// 1 10 11 10 undefined
foo( 10, undefined );	// 2 10 11 10 undefined
foo( 10, null );		// 2 10 null 10 null
```

While ES6 default parameter values can create divergence between the `arguments` array slot and the corresponding named parameter variable, this same disjointedness can also occur in tricky ways in ES5:

```js
function foo(a) {
	a = 42;
	console.log( arguments[0] );
}

foo( 2 );	// 42 (linked)
foo();		// undefined (not linked)
```

Note: **Never refer to a named parameter *and* its corresponding `arguments` slot at the same time.**

### `try..finally`

What happens if there's a `return` statement inside a `try` clause? It obviously will return a value, right? But does the calling code that receives that value run before or after the `finally`?

```js
function foo() {
	try {
		return 42;
	}
	finally {
		console.log( "Hello" );
	}

	console.log( "never runs" );
}

console.log( foo() );
// Hello
// 42
```

The exact same behavior is true of a `throw` inside `try`:

```js
 function foo() {
	try {
		throw 42;
	}
	finally {
		console.log( "Hello" );
	}

	console.log( "never runs" );
}

console.log( foo() );
// Hello
// Uncaught Exception: 42
```

```js
function foo() {
	try {
		return 42;
	}
	finally {
		// no `return ..` here, so no override
	}
}

function bar() {
	try {
		return 42;
	}
	finally {
		// override previous `return 42`
		return;
	}
}

function baz() {
	try {
		return 42;
	}
	finally {
		// override previous `return 42`
		return "Hello";
	}
}

foo();	// 42
bar();	// undefined
baz();	// "Hello"
```

Using a `finally` + labeled `break` to effectively cancel a `return` is doing your best to create the most confusing code possible.  

### `switch`

Coersive equality:  

```js
var a = "42";

switch (true) {
	case a == 10:
		console.log( "10 or '10'" );
		break;
	case a == 42:
		console.log( "42 or '42'" );
		break;
	default:
		// never gets here
}
// 42 or '42'
```
