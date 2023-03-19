
export default class connect{

    static connectToBackend()
    {
        return fetch('http://localhost:5000/connect', {
            'method': 'POST',
            headers : {
                'Content-Type':'application/json'
        },
        body: JSON.stringify("connect")
    })
        .then(response => response.json())
        .catch(error => console.log(error))
    }

}