/* eslint-disable */
export function LoadTweets(callback){
    const xhr = new XMLHttpRequest()
    const method = "GET"
    const djurl = "http://localhost:8000/api/tweets/"
    const responseType = "json"
    xhr.responseType = responseType
    xhr.open(method, djurl)
    xhr.onload = function(){
        callback(xhr.response, xhr.status)
    },
    xhr.onerror = function(error) {
      console.log(error)
      callback({'message': 'The request was an error'}, 400)
    }
    xhr.send()
  }