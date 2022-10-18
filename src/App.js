import logo from './logo.svg';
import './App.css';
import axios from "axios"
import {useEffect, useState} from "react";
import { Link } from 'react-router-dom'


function App() {

    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    var Repos;

    const onChange = (e) => {
    e.preventDefault();
    setResults([])

    setQuery(e.target.value);
    console.log(e.target.value)
    console.log("change recorded");
    }

     const lookUpDB = () => {

     axios.get("http://0.0.0.0:8000/db_repositories?username="+ query)
    .then((response) => {
        console.log(response.data);
        if(response.status=500)  { setResults([])}

            Repos = response.data["repositories"].map(repo => (<a href={repo['repo_link'].replace("git", "https")}>
                <div className="box"><p>{repo['repository_name']}</p></div>
            </a>))
            setResults([Repos])
        console.log(Repos);

    });


  };
     const lookUpGitHub = () => {

     axios.get("http://0.0.0.0:8000/repositories?username="+ query)
    .then((response) => {
        console.log(response.data);
        if(response.status=500)  { setResults([])}

            Repos = response.data["repositories"].map(repo => (<a href={repo['repo_link'].replace("git", "https")}>
                <div className="box"><p>{repo['repository_name']}</p></div>
            </a>))
            setResults(Repos)

    });};

  return (
    <div className="App">
      <p>Hello</p>
         <input
              type="text"
              placeholder="Search for a Profile"
              value={query}
              onChange={onChange}
            />
        <button onClick={lookUpDB}>Search DB</button>
        <button onClick={lookUpGitHub}>Search GitHub</button>
        {results}
    </div>
  );
}

export default App;
