export const post = (data) => {
    const response = fetch('http://127.0.0.1:8000/searchclass', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data), 
        /*body: JSON.stringify({
            "classstr": "",  // Edited
            "majorstr": ""
        }), //use JSON.stringify if and when needed, but currently string */
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