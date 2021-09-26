let widthNow

export function contentWidthSet(e) {
    const {value} = e.target
    localStorage.setItem("contentWidth", value)
    return (widthNow = value)
}

export function contentWidthGet() {
    return widthNow || (widthNow = localStorage.getItem("contentWidth")) || (widthNow = 100)
}