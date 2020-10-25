import React,{useEffect, useState} from 'react'
import {ProSidebar, Menu, MenuItem, SubMenu} from 'react-pro-sidebar'
import {Link} from 'react-router-dom'
import school_icon from './image/school_icon.jpg'
import 'react-pro-sidebar/dist/css/styles.css'
import './Navbar.scss'
import './DashBoard.css'
import game from './image/game.jpg'
import logit from './image/logit.png'

const DashBoard =(props) => {
    return (
        <div className="dashboard-main" style={{backgroundColor:"black"}}>
            <div className="dashboard-title">
                <h1>Unethical reporter</h1>
            </div>
            <div className="dashboard-title">
                <a href="https://github.com/MartianSheep/Unethical_Reporter" >GET IT NOW</a>
            </div>
            <div className="dashboard-text">
                <img src={game} alt="games" width="400px" height="350px"></img>
                <ul>
                    <li><p>Players can report others' unethical action to game managers in an easier way.</p></li>
                    <li><p>Game managers can get the information be sent from players properly.</p></li>
                    <li><p>We can verify when a person spoke dirty words via the information be sent.</p></li>
                </ul>
            </div>
            <div className="dashboard-text">
                <ul>
                    <h3>Recommand Device</h3>
                    <li><p>Logitech Pro Headset</p></li>
                    <li><p>Logitech G815 Harpy corded keyboard</p></li>
                    <li><p>Blue mic</p></li>
                    <h3>Recommand OS</h3>
                    <li>Windows 10</li>
                </ul>
                <img src={logit} alt="logit" width="400px" height="350px"></img>
            </div>
        </div>
    )
}

export default DashBoard