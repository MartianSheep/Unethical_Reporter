import React, {useState} from 'react'
import './Report.css'

const Report = (props) => {
    // props.match.params.reportID

    const playerID = props.match.params.playerID
    const reportID = props.match.params.reportID

    const ping = 34 //for test
    const title = "Title" //for test
    const platform = "Window X"
    const kb_input = "a g e g w v ty e h r4 s h e"
    const video_src = "#"


    let bgColor = ""

    if(ping<30){
        bgColor = "rgba(160,250,150, 0.5)"
    }else if(30 < ping && ping < 100){
        bgColor = "rgba(249,250,179, 0.6)"
    }else{
        bgColor = "rgba(250,198,195,0.6)"
    }


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