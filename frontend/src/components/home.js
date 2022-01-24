import React, { useState, useEffect } from "react";

const Home = () => {
    const [loggedIn, setLoggedIn] = useState(false);
    const [imageURL, setImageURL] = useState("");
    const [userName, setUserName] = useState("");
    const [term, setTerm] = useState("short_term");
    const [type, setType] = useState("artists")

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
    


    return (
        <div>
            <div className="login-container" id="login-container">
                <div className="title" id="title">
                </div>
                <div className="login">
                    <a href="http://127.0.0.1:8000/api/v1/login" id="login"></a>
                </div>
            </div>
            <div className="container">
                <dive className="info-tab">
                    <div className="profile-image-box">
                        <img className="profile-image" src={imageURL} alt=""/>
                    </div>
                    <div className="right-tab">
                        <div className="user-name" id="user-name">
                        </div>
                        <div className="term-buttons">
                            <div className="term-button">
                                Short Term
                            </div>
                            <div className="term-button">
                                Medium Term
                            </div>
                            <div className="term-button">
                                Long Term
                            </div>
                        </div>
                    </div>
                </dive>
            </div>
        </div>
    );
};

export default Home