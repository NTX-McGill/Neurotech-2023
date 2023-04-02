
export default class connect{

    static connectToBackend(timestamps)
    {
        return fetch('http://localhost:5000/connect', {
            'method': 'POST',
            headers : {
                'Content-Type':'application/json'
        },
        body: JSON.stringify(timestamps)
    })
        .catch(error => console.log(error))
    }

}