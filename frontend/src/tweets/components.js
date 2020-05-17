/* eslint-disable */
import React, {useEffect, useState} from 'react'
import {LoadTweets} from '../lookup'

export function TweetsComponent(props) {
  const textAreaRef = React.createRef()
  const [newTweets, setNewTweets] = useState([])
  const handleSubmit = (event) =>{
    event.preventDefault()
    // console.log(event)
    const newTweet = textAreaRef.current.value
    let newTempTweets = [...newTweets]
    newTempTweets.unshift({
      content: newTweet,
      like: 0,
      id: 211
    })
    setNewTweets(newTempTweets)
    // console.log(newTweet)
    textAreaRef.current.value = ''
  }  
  return <div className={props.className}>
    <div className='col-12 mb-3'>
      <form onSubmit={handleSubmit}>
        <textarea ref={textAreaRef} required={true} className='form-control' name="tweet"></textarea>
        <button type="submit" className="btn btn-primary my-3">Tweet</button>
      </form>
    </div>
    <TweetsList newTweets={newTweets}/>
  </div>
}

export function TweetsList(props){
  console.log(props.newTweets)
  const [tweetInit, setTweetInit] = useState([])
  const [tweetList, setTweetList] = useState([])
  useEffect(() => {
    const final = [...props.newTweets].concat(tweetInit)
    if(final.length !== tweetList.length){
      setTweetList(final)
    }
  }, [props.newTweets, tweetList, tweetInit])
  useEffect(()=>{
    const myCallback =(response, status)=>{
      // console.log(response, status)
      if(status === 200){
        // const finalTweetList = [...response].concat(tweetInit)
        setTweetInit(response)
      }
    }
    LoadTweets(myCallback)
  }, [tweetInit])
  return tweetList.map((item,index)=>{
    return <Tweet tweets={item} className="py-5 my-5 border bg-white text-dark" key={`${index}-${item.id}`}/>
  })
}

export function ActionButton(props){
    const {tweet, action} = props
    const [likes, setLikes] = useState(tweet.like ? tweet.like : 0)
    const [userlike, setUserlike] = useState(tweet.userlike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary'
    const ActionDisplay = action.display ? action.display : 'Action'
    const display = action.type === 'like' ? `${likes} ${ActionDisplay}` : `${ActionDisplay}`
    const handleClick = (event)=>{
      event.preventDefault()
      if(action.type === 'like'){
        if(userlike === true){
          setLikes(likes-1)
          setUserlike(false)
        }else{
          setLikes(likes+1)
          setUserlike(true)
        }
      }
    }
return <button className={className} onClick={handleClick}>{display}</button>
  }

export function Tweet(props) {
    const {tweets} = props
    const className = props.className ? props.className : "col-10 mx-auto col-md-6"
    const action = {type: 'like'}
    return <div className={className}>
      <p>{tweets.id} - {tweets.content}</p>
      <div className='btn btn-group'>
        <ActionButton tweet={tweets} action={{type: 'like', display: 'Like'}}/>
        <ActionButton tweet={tweets} action={{type: 'unlike', display: 'Unlike'}}/>
        <ActionButton tweet={tweets} action={{type: 'retweet', display: 'Retweet'}}/>
      </div>
    </div>
  }