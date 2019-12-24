title: Some Form dealing about Promise and Component in Ant Design (React.js)
date: 2019-12-13 21:49
modified: 2019-12-24 22:44
author: Sim
tags: Ant Design, React.js, Javascript, wrappedComponentRef, Promise, Form
summary: Recently I've been working with React and Ant Design at work. React is a pretty flexible framework to work with, while Ant Design is a comprehensive framework like Bootstrap. Although i need sometime to adapt to it. 

## wrappedComponentRef

This is especially useful when I need a component to fetch something from another.  

```js
import React from 'react'
// ...
class Something extends React.Component {
    ...
    render() {
        return (
            <div>
                <RefedComponent wrappedComponentRef={(inst)=> this.TheRef = inst} />
                <TheComponent content={this.TheRef.content}>
            </div>
            )
    }
}

```

It's especially useful when I want to deal with the form in a modal.  

## Promise Chain

It's really important either in JS or React or any other JS environment to deal with ajax requests like `POST`.  

In some scenes I need tree to be loaded according to my need, that's when promise chain come into use.  

For example I need a function that returns a Promise in `loadData` attribute in `<TreeSelect>`:

```js
//...
    onLoadData = treeNode => {
        let _this = this
        return new Promise(resolve => {
            // ...
            getAreaOptions({parentId: id}).then(res=> {
                let result = res.data.result.map(item=>{
                    return {
                        id:item.id,
                        value:item.id,
                        key:item.id,
                        pId:item.parentId,
                        title:item.name,
                        isLeaf:item.level==3,
                        selectable:item.level==3
                    }
                })
                //...
                resolve(result)
            })
        }).then(result=>{
            _this.setState({
                treeData: result,
            })
        });
    }
//...
```

## A component whose value can be obtained through the Form

The example on the official website[^1] says everything:  

```js hl_lines="44 45 46 47 48 49 50 51 52 53"
import { Form, Input, Select, Button } from 'antd';

const { Option } = Select;

class PriceInput extends React.Component {
  static getDerivedStateFromProps(nextProps) {
    // Should be a controlled component.
    if ('value' in nextProps) {
      return {
        ...(nextProps.value || {}),
      };
    }
    return null;
  }

  constructor(props) {
    super(props);

    const value = props.value || {};
    this.state = {
      number: value.number || 0,
      currency: value.currency || 'rmb',
    };
  }

  handleNumberChange = e => {
    const number = parseInt(e.target.value || 0, 10);
    if (isNaN(number)) {
      return;
    }
    if (!('value' in this.props)) {
      this.setState({ number });
    }
    this.triggerChange({ number });
  };

  handleCurrencyChange = currency => {
    if (!('value' in this.props)) {
      this.setState({ currency });
    }
    this.triggerChange({ currency });
  };

  triggerChange = changedValue => {
    // Should provide an event to pass value to Form.
    const { onChange } = this.props;
    if (onChange) {
      onChange({
        ...this.state,
        ...changedValue,
      });
    }
  };

  render() {
    const { size } = this.props;
    const { currency, number } = this.state;
    return (
      <span>
        <Input
          type="text"
          size={size}
          value={number}
          onChange={this.handleNumberChange}
          style={{ width: '65%', marginRight: '3%' }}
        />
        <Select
          value={currency}
          size={size}
          style={{ width: '32%' }}
          onChange={this.handleCurrencyChange}
        >
          <Option value="rmb">RMB</Option>
          <Option value="dollar">Dollar</Option>
        </Select>
      </span>
    );
  }
}
```

However `getDerivedStateFromProps` is kinda dated and not recommended in React now[^2] and could lead to some issues. Generally to acheive the things above I would rewrite the code to make the component fully controlled like the officially recommended way:  

```js hl_lines="19 20 21 22 23 24 25 26 27 28 29"
import { Form, Input, Select, Button } from 'antd';

const { Option } = Select;

class PriceInput extends React.Component {

  handleNumberChange = e => {
    const number = parseInt(e.target.value || 0, 10);
    if (isNaN(number)) {
      return;
    }
    this.triggerChange({ number });
  };

  handleCurrencyChange = currency => {
    this.triggerChange({ currency });
  };

  triggerChange = changedValue => {
    // Should provide an event to pass value to Form.
    const { onChange, number, currency } = this.props;
    if (onChange) {
      onChange({
        number,
        currency,
        ...changedValue,
      });
    }
  };

  renderThing(props) {
    const { size, currency, number } = props;
    return (
      <span>
        <Input
          type="text"
          size={size}
          value={number}
          onChange={this.handleNumberChange}
          style={{ width: '65%', marginRight: '3%' }}
        />
        <Select
          value={currency}
          size={size}
          style={{ width: '32%' }}
          onChange={this.handleCurrencyChange}
        >
          <Option value="rmb">RMB</Option>
          <Option value="dollar">Dollar</Option>
        </Select>
      </span>
    );
  }

  render() {
    return renderThing(this.props)
  }
}
```

## componentDidUpdate: make changes towards value changes in props or state

```
import React from 'react'

class something extends React.Components {
  \\...
  componentDidUpdate(prevProps, prevState) {
    console.log('The previous props of the component: ' + prevProps + '\nThe current props of the component: ' + this.props)
    console.log('The previous props of the component: ' + prevProps + '\nThe current props of the component: ' + this.props)
  }
  \\...
}

export default something
```

This is a really useful thing in React Lifecycle.  

I can use it to:  

1. Monitor the changes in the state in the component and do something according to it
2. Monitor the changes in the props in the component and do something according to it
3. Do something as long as the data changes.  

It's like the `watcher` and `computed` in the Vue.

[^1]: [Form - Ant Design](https://ant.design/components/form/#components-form-demo-customized-form-controls)
[^2]: [You Probably Don't Need Derived State – React Blog](https://reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html)