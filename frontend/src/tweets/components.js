/* eslint-disable */
import React, {useEffect, useState} from 'react'
import {LoadTweets} from '../lookup'

export function TweetsList(props){
  const [tweets, setTweets] = useState([])
  useEffect(()=>{
    const myCallback =(response, status)=>{
      // console.log(response, status)
      if(status === 200){
        setTweets(response)
      }
    }
    LoadTweets(myCallback)
  }, [])
  return tweets.map((item,index)=>{
    return <Tweet tweets={item} className="py-5 my-5 border bg-white text-dark" key={`${index}-${item.id}`}/>
  })
}

export function ActionButton(props){
    const {tweet, action} = props
    const [likes, setLikes] = useState(tweet.like ? tweet.like : 0)
    const [justClicked, setJustClicked] = useState(false)
    const className = props.className ? props.className : 'btn btn-primary'
    const ActionDisplay = action.display ? action.display : 'Action'
    const display = action.type === 'like' ? `${likes} ${ActionDisplay}` : `${ActionDisplay}`
    const handleClick = (event)=>{
      event.preventDefault()
      if(action.type === 'like'){
        if(justClicked === true){
          setLikes(likes-1)
          setJustClicked(false)
        }else{
          setLikes(likes+1)
          setJustClicked(true)
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