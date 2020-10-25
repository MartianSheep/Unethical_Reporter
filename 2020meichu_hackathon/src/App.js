import React,{useState, useEffect} from 'react'
import './App.css';
import {Route} from 'react-router-dom'
import Report from './Report'
import Navbar from './Navbar'

import axios from 'axios'

const server_source = 'https://unethicalreporter.martiansheep.repl.co/'

const App = (props) => {

  const [playerIDs, setPlayerIDs] = useState([])

  const getPlayerIDs = () => {
    axios.get(server_source+'report_ids',{})
    .then(data=>setPlayerIDs(data.data))
    .catch(error=>console.log(error))
  }

  //======Test========
  // const testArray = () => {
  //   setPlayerIDs(
  //     {
  //       "1234":["1","4u","3983","e979"],
  //       "843":["ei","r387wy","e8y","eufyue"],
  //       "eie":["iwhe","e8ye","1367dn","28ed"]
  //     }
  //   )
  // }
  //======Test========


  useEffect(()=>{
    getPlayerIDs()
    // testArray() //for test
  },[])

  return(
    <div>
      <Navbar playerIDs={playerIDs}/>
      <Route path="/reports/:playerID/:reportID" component={Report}></Route>
    </div>
  )
}

export default App;
