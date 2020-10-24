import React,{useEffect, useState} from 'react'
import {ProSidebar, Menu, MenuItem, SubMenu} from 'react-pro-sidebar'
import {Link} from 'react-router-dom'
import school_icon from './image/school_icon.jpg'
import 'react-pro-sidebar/dist/css/styles.css'
import './Navbar.scss'
import './DashBoard.css'
const DashBoard =(props) => {
    return (
        <div className="dashboard-main" style={{backgroundColor:"black"}}>
            <div className="dashboard-title">
                <h1>Unethical report</h1>
            </div>
            <div className="dashboard-title">
                <a href="https://github.com/MartianSheep/Unethical_Reporter" >GET IT NOW</a>
            </div>
            <div className="dashboard-title">
                Functions
                <ul>
                    <li>Let players report others' unethical action to game manager in an easier way</li>
                    <li></li>
                </ul>
            </div>
        </div>
    )
}

export default DashBoard