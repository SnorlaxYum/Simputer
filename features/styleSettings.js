let widthNow
let ToCOn

export function contentWidthSet(e) {
    const {value} = e.target
    localStorage.setItem("contentWidth", value)
    return (widthNow = value)
}

export function contentWidthGet() {
    return widthNow || (widthNow = localStorage.getItem("contentWidth")) || (widthNow = 100)
}

export function ToCOnSet(e) {
    const {checked} = e.target
    localStorage.setItem("ToCOn", checked)
    return (ToCOn = checked)
}

export function ToCOnGet() {
    if(typeof ToCOn === "boolean") {
        return ToCOn
    }
    const valueNow = localStorage.getItem("ToCOn")
    if(typeof valueNow !== "object") {
        return (ToCOn = valueNow === "true")
    }
    return (ToCOn = true)
}