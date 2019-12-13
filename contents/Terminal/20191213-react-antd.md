title: Some Form dealing about Promise and Component in Ant Design (React.js)
date: 2019-12-13 21:49
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

```js hl_lines="6 7 8 9 10 11 12 13 14 44 45 46 47 48 49 50 51 52 53"
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

[^1]: [Form - Ant Design](https://ant.design/components/form/#components-form-demo-customized-form-controls)