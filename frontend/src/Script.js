//https://gist.github.com/justsml/529d0b1ddc5249095ff4b890aad5e801

function Script() {
    //console.log("hello Shivika");

    fetch('http://localhost:3000')
        .then(response => {
        //handle response            
        console.log(response);
        })
        .then(data => {
        //handle data
        console.log(data);
        })
        .catch(error => {
        //handle error
        });

    fetch('http://localhost:3000', {
        Method: 'POST',
        Headers: {
            Accept: 'application.json',
            'Content-Type': 'application/json'
        },
        Body: 'Hi shivika',
        Cache: 'default'
        })
} 
export default Script;

/*

getRequest('http://localhost:3000')
.then(data => {
  console.log(data) // Prints result from `response.json()` in getRequest
})
.catch(error => console.error(error))

function getRequest(url) {
return fetch(url, {
    ////handle response
    })
.then(response => response.json())
}


postRequest('http://localhost:3000')
.then(data => console.log(data)) // Result from the `response.json()` call
.catch(error => console.error(error))

function postRequest(url) {
return fetch(url, {
    credentials: 'same-origin', // 'include', default: 'omit'
    method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
    body: 'Insert Body Here', // Coordinate the body type with 'Content-Type'
    headers: new Headers({
    'Content-Type': 'application/json'
    }),
})
.then(response => response.json())
}
*/

//////////////////////////////////////////////////////////////

/*
async function getData()
{
    const data = document.getElementById("dataValue").value;
    console.log(data); 

    const endpoint = new URL("http://localhost:3000");
    console.log(endpoint); 

    const response = await fetch(endpoint); 
    console.log(response); 
}
getData();
 */
/////////////////////////////////////////////

/*
console.log("Hello")

componentDidMount () 
{
    const data = document.getElementById("dataValue").value;
    console.log(data); 

    const endpoint = new URL("http://localhost:3000");
    console.log(endpoint); 

    const response = await fetch(endpoint); 
    console.log(response);
}


fetch('http://localhost:3000', {
    method: 'get',
    headers: new Headers
    ({
        'Content-Type': 'application/x-www-form-urlencoded',
    }),
}).then((response) => {
    if (!response.ok) {
        throw response;
    }
    console.log("SUCCESSFUL")
    return response.json()
}).catch((error) => {
        console.log("Not Succesful"); //setWorkspaces(error.toString());
    });


*/

/*

 getResult.then((response) => {
    if (!response.ok) {
        throw response;
    }
    return response.json();
    })
    .then((json) => {
    //setChannel(json);
        console.log('SUCCESS')//localStorage.setItem('channels', JSON.stringify(json));
    })
    .catch((error) => {
        console.log("Not Succesful")//setChannel(error.toString());
//////////////////////////////

const postResult = fetch ('http://localhost:3000', {
    method: 'POST',
    headers: 
    {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'User 1'
    })
}).then(res => {
    if (res.ok){
        console.log('SUCCESS')
    } else {
        console.log("Not Succesful")
    }
    return res.json
    })
    .then(data => console.log(data))
    .catch(error => console.log('ERROR'))

*/