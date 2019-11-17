---
title: Notes on Async & Performance (YDJS)
author: Sim
tags: js, You don't know Js, learning notes
status: published
summary: "Notes on You Don't Know JS: Async & Performance."
date: 2019-05-17 17:00
modified: 2019-05-19 22:00
Series: You Don't Know JS Read Note
---

Seems I've taken rather complicated note one the last one.

## Chapter 1: Asynchrony: Now & Later

One of the most essential parts in language like ja is about how to express and manipulate program over time. Before getting there, it's helpful to understand much more deeply what asynchrony is and how it operates in JS.

### A Program in Chunks

_now_ chunk: stuff that runs now.  
_later_ chunk: stuff that runs later.

#### Async Console  

`console.log` differs between different browsers. Some doesn't output the result immediately.  

### Event Loop

It acts as a queue, first-in, first-out.  

### Parallel Threading

In a parallel system, avoid the different actions on the same variable, which might lead to unexpected results (different orders, different results on the same codes).

`race condition`: function ordering nondeterminism.

### Concurrency

The single-threaded event loop is one expression of concurrency with sequential results.  

#### Noninteracting

If two concurrent processes act independently, the code will behave right regardless of ordering.  

#### Interaction

Do things to coordinate interactions between processes:  

1. Push two individuals into the array(`arrvar.push(thing)`) and make sure the order: determine the order in advance
2. Assign value to var a and var b in different processes and need them both at the same time: make sure `a && b` returns true in `if`.
3. Different call on the same variable `a` and may cause unexpected result: `if (a == undefined)`

#### Cooperation

An Ajax response handler that needs to run through a long list of results to transform the values:  

```js
var res = [];

// `response(..)` receives array of results from the Ajax call
function response(data) {
	// let's just do 1000 at a time
	var chunk = data.splice( 0, 1000 );

	// add onto existing `res` array
	res = res.concat(
		// make a new transformed array with all `chunk` values doubled
		chunk.map( function(val){
			return val * 2;
		} )
	);

	// anything left to process?
	if (data.length > 0) {
		// async schedule next batch
		setTimeout( function(){
			response( data );
		}, 0 );
	}
}

// ajax(..) is some arbitrary Ajax function given by a library
ajax( "http://some.url.1", response );
ajax( "http://some.url.2", response );
```

`setTimeout(..0)` is not technically inserting an item directly onto the event loop queue. The timer will insert the event at its next opportunity. Not guaranteed to process in call order. There's not a single direct way (at least yet) across all environments to ensure async event ordering. This topic will be covered in more detail in the next section.

### Jobs  

`Job Queue`: New concept in ES6. Make the job implemented **later, but as soon as possible**.  

### Statement Ordering

The order in which we express statements in our code is not necessarily the same order as the JS engine will execute them. That may seem like quite a strange assertion to make.  

## Chapter 2: Callbacks

`callback`: the target for the event loop to "call back into" the program, whenever that item in the queue is processed.  

The callback function is the async work horse for JavaScript, and it does its job respectably. A couple of these is explored in the chapter.  

### Continuations

First half executes immediately, then pause at the callback function to get the response, then continue with the second half.  

### Sequential Brain

JS would probably feel like a sequential brain, switching to various different processes constantly.  

#### Doing Versus Planning

The reason it's so hard to accrately author and reason about async JS code with callbacks: it's not how our brain works.  

#### Nested/Chained Callbacks

`callback hells`: callback continuations are happening *simultaneously*.  

### Trust Issues

`inversion of control`: you take part of your program and give over control of its execution to another third party  

#### Tale of Five Callbacks

Investing an awful lot of ad hoc logic **in every and single callback** leads to `callback hell`.  

#### Not Just Others' Code

Necessary to do *inversion of control*.

### Trying to Save Callbacks

trust issues:  

1. There's nothing about either callback that prevents or filters unwanted repeated invocations.  
2. Being never called
3. Too Early

ES6 has arrived on the scene with some great answers to these trust issues.  

### Review

We need a generalized solution to **all of the trust issues**, one that can be reused for as many callbacks as we create without all the extra boilerplate overhead.

We need something better than callbacks. They've served us well to this point, but the *future* of JavaScript demands more sophisticated and capable async patterns.

## Chapter 3: Promises

To b continued......
