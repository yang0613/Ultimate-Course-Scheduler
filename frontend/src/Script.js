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
    console.log(JSON.stringify(data));
    const response = fetch('http://127.0.0.1:8000/verification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data), 
    })
    return response
}

export const login = (data) => {
    const response = fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),  
    })
    return response
}

export const register = (data) => {
    const response = fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),   
    })
    return response
}

export const storePlan = (data) => {
    const response = fetch('http://127.0.0.1:8000/academicplan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),   
    })
    return response
}