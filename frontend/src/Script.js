export const post = (data) => {
    const response = fetch('http://127.0.0.1:8000/searchclass', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            "classstr": "cse 101",
            "majorstr": ""
        }, //use JSON.stringify if and when needed, but currently string
    })
    return response
}

//const [input, setInput] = React.useState({"classstr": "", "majorstr": ""});

/*const data = {
            "classstr": "cse 101",
            "majorstr": ""
       } */

export const get = (data) => {
    //const response = fetch(`http://127.0.0.1:8000/searchclass?data=${data}`,{
    const response = fetch(`http://127.0.0.1:8000/searchclass`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    return response
}


// ================================================================================================
// Ignore everything below this --- was experimenting with the code structure 
// while learning how to properly write the fetch calls
// ================================================================================================

// https://gist.github.com/justsml/529d0b1ddc5249095ff4b890aad5e801
/*
function Script() 
{
    console.log("hello Shivika");

    
    fetch('http://127.0.0.1:8000/searchclass', {
        Method: 'POST',
        Headers: {
            Accept: 'application.json',
            'Content-Type': 'application/json'
        },
        Body: 'Hi shivika',
        Cache: 'default'
    })

    //Integration
    const [input, setInput] = React.useState({"classstr": "", "majorstr": ""});

    const handleInput = (event) => {
        const {value, name}= event.target;
        const i = input;
        i[name] = value;
        setInput(i);
    }
}

//     const handleFetch = (event) => {
//     fetch('/searchclass', {
//         Method: 'GET',
//         Headers: {
//             Accept: 'application.json',
//             'Content-Type': 'application/json'
//         },
//         Body: JSON.stringify(input),
//         Cache: 'default'
//         })
//         .then(response => {
//         //handle response            
//         return response.json();
//         })
//         .then((data) => {
//             console.log(JSON.stringify(data));
//           })
//         .catch(error => {
//         //handle error
//             console.log(error);
//             alert(error);
//         });
//     };
// }
// export default Script;

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
/*

function Script() 
{
    var jsonData = {
      "users": [
          {
              "name": "alan", 
              "age": 23,
              "username": "aturing"
          },
          {
              "name": "john", 
              "age": 29,
              "username": "__john__"
          }
      ]
    }
  
    function handleClick() {
      
      // Send data to the backend via POST
      fetch('http://------------:8080/', {  // Enter your IP address here
  
        method: 'POST', 
        mode: 'cors', 
        body: JSON.stringify(jsonData) // body data type must match "Content-Type" header
  
      })
      
    }
  
    return (
      <div onClick={handleClick} style={{
        textAlign: 'center',
        width: '100px',
        border: '1px solid gray',
        borderRadius: '5px'
      }}>
        Send data to backend
      </div>
    );
}
  
export { Script };

*/