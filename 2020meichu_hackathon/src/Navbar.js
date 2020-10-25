import React,{useEffect, useState} from 'react'
import {ProSidebar, Menu, MenuItem, SubMenu} from 'react-pro-sidebar'
import {Link} from 'react-router-dom'
import school_icon from './image/school_icon.jpg'
import 'react-pro-sidebar/dist/css/styles.css'
import './Navbar.scss'
import DashBoard from './DashBoard'

const Navbar = (props) => {

    let options = []

    const renderOptions = () => {
        // console.log(":XD")
        // console.log(props.reportIDs)
        console.log(props.playerIDs)
        let arr = Object.keys(props.playerIDs).map(
            playerID => {
                return(<PlayerReports key={playerID} playerID={playerID} reports={props.playerIDs[playerID]} />)
            }
        )
        options = arr
        
    }

    renderOptions()

    

    return(
        <ProSidebar>
            <Menu iconShape='round'>
                <MenuItem>
                    <div style={{display:'flex', margin:"auto", justifyContent:"center"}}>
                        <img style={{borderRadius:"50%"}}src={school_icon} alt="school_icon" width="200px" height="200px"></img>
                    </div>
                </MenuItem>
                <MenuItem>
                    <p style={{fontSize:"30px", margin:"0", textAlign:'center'}}>
                        G-key Reporting System
                    </p>
                </MenuItem>
                <MenuItem>DashBoard<Link to="/dashboard"/></MenuItem>
                <MenuItem>Team Members <Link to="/team"/></MenuItem>
                <SubMenu title="All Reports">
                    {options}
                </SubMenu>
            </Menu>
        </ProSidebar>
    )
}

const PlayerReports = (props) => {
    // console.log(props.reports)
    let reports = props.reports.map(
        reportID => {
            return(
                <MenuItem key={reportID}>
                    {reportID}
                    <Link to={"/reports/"+props.playerID+"/"+reportID}/>
                </MenuItem>
            )
        }
    )

    return(
        <SubMenu title={props.playerID} key={props.playerID}>
            {reports}
        </SubMenu>
    )
}

export default Navbar