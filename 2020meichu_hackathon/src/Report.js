import axios from 'axios'
import React, {useEffect, useState} from 'react'
import './Report.css'

const cors = 'https://cors-anywhere.herokuapp.com/'; // use cors-anywhere to fetch api data
const server_source = 'https://unethicalreporter.martiansheep.repl.co/'

const Report = (props) => {
    // props.match.params.reportID

    const playerID = props.match.params.playerID
    // const reportID = props.match.params.reportID
    const reportID  = 1 //for test

    // const ping = 34 //for test
    // const title = "Title" //for test
    // const platform = "Window X"
    // const kb_input = "a g e g w v ty e h r4 s h e"
    // const video_src = "#"

    const [ping, setPing] = useState(0)
    const [title, setTitle] = useState('')
    const [platform, setPlatform] = useState('')
    const [kb_input, setKbInput] = useState('')
    const [video_src, setVideoSrc] = useState(null)


    let bgColor = ""

    if(ping<30){
        bgColor = "rgba(160,250,150, 0.5)"
    }else if(30 < ping && ping < 100){
        bgColor = "rgba(249,250,179, 0.6)"
    }else{
        bgColor = "rgba(250,198,195,0.6)"
    }

    
    const getJSONfiles = () => {
        axios.get(`${cors}${server_source+'report_json/'+reportID+'/dev_json.json'}`,{report_id:reportID, filename:'dev_json.json'}, {mode:'no-cors'})
        .then(data => console.log(data))
        .catch(error => console.log(error))

        axios.get(`${cors}${server_source+'report_json/'+reportID+'/kb_input.json'}`,{report_id:reportID, filename:'kb_input.json'}, {mode:'no-cors'})
        .then(data=> setKbInput(data.data["0"]))
        .catch(error => console.log(error))

        axios.get(`${cors}${server_source+'report_json/'+reportID+'/info.json'}`,{report_id:reportID, filename:'info.json'}, {mode:'no-cors'})
        .then(data=> {setPing(data.data.ping)
                    setPlatform(data.data.platform)})
        .catch(error => console.log(error))
    }

    const getVideos = () => {

    }

    useEffect(()=>{
        getJSONfiles()
    })

    return(
        <div className="report-main container" style={{backgroundColor:bgColor}}>
            <div className="report-title">
                <p style={{textAlign:"center"}}>{title}</p>
            </div>
            
            <video className="video-container" width="800" height="480" controls>
                <source src={video_src} type="video/mp4"/>
            Your browser does not support the video tag.
            </video>
            <div className="kb-input-container">
                <p className="kb-input">
                    {kb_input}
                </p>
            </div>
            <div className="platform">
                {platform}
            </div>
            <div className="ping">
                Ping:{ping}
            </div>
        </div>
    )
}

export default Report