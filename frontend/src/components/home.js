import React, { useState, useEffect } from "react";

const Home = () => {
    const [loggedIn, setLoggedIn] = useState(false);
    const [imageURL, setImageURL] = useState("");
    const [userName, setUserName] = useState("");
    const [term, setTerm] = useState("short_term");
    const [type, setType] = useState("tracks");
    const [data, setData] = useState({})
    const [box, setBox] = useState([])

    useEffect( () => {
        const CURRENT_URL_QUERY = window.location.search;
        const URL_PARAMS = new URLSearchParams(CURRENT_URL_QUERY);
        if (URL_PARAMS.get('user_id') != null) {
            localStorage.user_id = URL_PARAMS.get('user_id');
            window.location.href = './';
        }
    });

    useEffect( () => {
        if (localStorage.user_id != null) {
            setLoggedIn(true);
            fetch("/api/v1/retrieve-info", {
                method: "POST",
                headers: {
                    'Content-Type':'application/json',
                    'Accept':'application/json',
                },
                body: JSON.stringify({
                    'user_id': localStorage.user_id,
                }),
            })
            .then( (response) => response.json())
            .then( (response) => {
                console.log(response)

                const resJson = JSON.parse(response);

                let user_name = document.getElementById('user-name')

                setImageURL(resJson.user_image_url);
                setUserName(resJson.user_name);
                setData(resJson)
                setBox(resJson.user_top_tracks_short_term_arr.slice(0, 48))
                console.log(userName)
                user_name.innerHTML = resJson.user_name;
            })
        }
    },[]);

    useEffect( () => {
        if (loggedIn) {
            let login_container = document.getElementById("login-container");
            login_container.parentNode.removeChild(login_container);
        } else {
            let title = document.getElementById("title")
            let login = document.getElementById("login")
            title.innerHTML = "Wave"
            login.innerHTML = "Log in with Spotify"
        }
    },[loggedIn]);

    const CHANGE_TYPE_ARTISTS = () => {
        let change = false
        if (type != "artists") {
            setType("artists")
            change = true
        }

        if (change) {
            setBox(data[('user_top_' + "artists" + '_' + term + '_arr')].slice(0, 48))
        }

    }

    const CHANGE_TYPE_TRACKS = () => {
        let change = false
        if (type != "tracks") {
            setType("tracks")
            change = true
        }

        if (change) {
            console.log(('user_top_' + "tracks" + '_' + term + '_arr'))
            setBox(data[('user_top_' + "tracks" + '_' + term + '_arr')].slice(0, 48))
        }

    }

    
    const CHANGE_TERM_SHORT = () => {
        let change = false
        if (term != "short_term") {
            setTerm("short_term")
            change = true
        }

        if (change) {
            setBox(data[('user_top_' + type + '_' + "short_term" + '_arr')].slice(0, 48))
        }

    }

    const CHANGE_TERM_MEDIUM = () => {
        let change = false
        if (term != "medium_term") {
            setTerm("medium_term")
            change = true
        }

        if (change) {
            setBox(data[('user_top_' + type + '_' + "medium_term" + '_arr')].slice(0, 48))
        }

    }

    const CHANGE_TERM_LONG = () => {
        let change = false
        if (term != "long_term") {
            setTerm("long_term")
            change = true
        }

        if (change) {
            setBox(data[('user_top_' + type + '_' + "long_term" + '_arr')].slice(0, 48))
        }

    }
    
    const BOX_MAPPER = (props) => {
        console.log(document.documentElement.clientHeight)
        return (
            <img src={props.box.image_url} alt="" className="box-image"/>
        )
    }


    return (
        <div>
            <div className="login-container" id="login-container">
                <div className="title" id="title">
                </div>
                <div className="login">
                    <a href="http://127.0.0.1:8000/api/v1/login" id="login"></a>
                </div>
            </div>
            <div className="container" style={{display: loggedIn ? 'flex' : 'none'}}>
                <dive className="info-tab">
                    <div className="profile-image-box">
                        <img className="profile-image" src={imageURL} alt=""/>
                    </div>
                    <div className="right-tab">
                        <div className="user-name" id="user-name">
                        </div>
                        <div className="term-buttons">
                            <button className="term-button" onClick={ () => CHANGE_TERM_SHORT()}>Recently</button>
                            <button className="term-button" onClick={ () => CHANGE_TERM_MEDIUM()}>Past Year</button>
                            <button className="term-button" onClick={ () => CHANGE_TERM_LONG()}>All Time</button>
                        </div>
                    </div>
                </dive>
                <div>
                <div class="tab-container">
                    <button className="tab-button" onClick={ () => CHANGE_TYPE_TRACKS()}>Top Tracks</button>
                    <button className="tab-button" onClick={ () => CHANGE_TYPE_ARTISTS()}>Top Artists</button>
                </div>
                </div>
                <div className="box-container">
                {
                    box.map( (box) => 
                    {
                        return <BOX_MAPPER box={box}/>
                    })
                }
                </div>
            </div>
        </div>
    );
};

export default Home