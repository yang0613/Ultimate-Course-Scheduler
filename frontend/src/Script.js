export const post = (data) => {
    const response = fetch('http://127.0.0.1:8000/searchclass', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data), 
    })
    return response
}

export const verify = (data) => {
    const response = fetch('http://127.0.0.1:8000/verification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data), 
    })
    return response
}

export const get = (data) => {
    const response = fetch(`http://127.0.0.1:8000/searchclass?data=${data}`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    return response
}