import React,{useEffect, useState} from 'react'
import {ProSidebar, Menu, MenuItem, SubMenu} from 'react-pro-sidebar'
import {Link} from 'react-router-dom'
import school_icon from './image/school_icon.jpg'
import 'react-pro-sidebar/dist/css/styles.css'
import './Navbar.scss'
import './TeamMember.css'

const TeamMember =(props) => {
    return (
        <div className="teammember-main" style={{backgroundColor:"black"}}>
            <div className="teammember-title">
                <h1>G-key Reporting System </h1>
            </div>
            <div className="teammember-title">
                <h2>國立陽明大學電機工程學系</h2>
            </div>
            <div className="teammember-title">
                <ul>
                    <li><p>任瑨洋 <a href="https://github.com/MartianSheep" >github</a></p></li>
                    <li><p>吳東昱 <a href="https://github.com/MartianSheep" >github</a></p></li>
                    <li><p>王友廷 <a href="https://github.com/MartianSheep" >github</a></p></li>
                    <li><p>張家翔 <a href="https://github.com/MartianSheep" >github</a></p></li>
                    <li><p>陳亮君 <a href="https://github.com/MartianSheep" >github</a></p></li>
                </ul>
            </div>
        </div>
    )
}

export default TeamMember