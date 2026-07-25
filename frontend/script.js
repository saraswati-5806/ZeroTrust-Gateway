/*=====================================================
        IBM ZERO TRUST SECURITY GATEWAY
              SCRIPT.JS PART 1
======================================================*/

document.addEventListener("DOMContentLoaded", function () {

    /*=====================================
            GET HTML ELEMENTS
    =====================================*/

    const loginScreen = document.getElementById("loginScreen");
    const dashboard = document.getElementById("dashboard");

    const loginBtn = document.getElementById("loginBtn");

    const userId = document.getElementById("userid");
    const password = document.getElementById("password");

    const loginError = document.getElementById("loginError");

    /*=====================================
            HIDE DASHBOARD
    =====================================*/

    dashboard.style.display = "none";

    /*=====================================
        LOGIN FUNCTION
    =====================================*/

    function loginUser() {

        const uid = userId.value.trim();
        const pass = password.value.trim();

        /* Remove previous error */

        loginError.textContent = "";

        userId.style.borderColor = "#9AC8E5";
        password.style.borderColor = "#9AC8E5";

        /* Check Credentials */

        if (uid === "IBM2026" && pass === "Model") {

            loginScreen.style.opacity = "0";

            setTimeout(function () {

                loginScreen.style.display = "none";

                dashboard.style.display = "block";

                dashboard.style.animation = "fadeIn 0.8s ease";

            }, 600);

        }

        else {

            loginError.textContent =
                "Invalid User ID or Password";

            userId.style.borderColor = "#D9534F";

            password.style.borderColor = "#D9534F";

        }

    }

    /*=====================================
        LOGIN BUTTON
    =====================================*/

    loginBtn.addEventListener("click", loginUser);

    /*=====================================
        ENTER KEY LOGIN
    =====================================*/

    password.addEventListener("keypress", function (event) {

        if (event.key === "Enter") {

            loginUser();

        }

    });
/*=====================================================
        SCRIPT.JS PART 2
    DASHBOARD INTERACTIONS
======================================================*/

/*=====================================
        LIVE DATE & TIME
=====================================*/

function updateDateTime() {

    const now = new Date();

    const options = {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    };

    const dateText = now.toLocaleDateString("en-US", options);
    const timeText = now.toLocaleTimeString();

    const headerText = document.querySelector(".header-left p");

    if(headerText){

        headerText.innerHTML =
        "Enterprise Cyber Security Dashboard | " +
        dateText + " | " + timeText;

    }

}

updateDateTime();

setInterval(updateDateTime,1000);

/*=====================================
        ACTIVE SIDEBAR
=====================================*/

const menuItems = document.querySelectorAll("aside ul li");

menuItems.forEach(function(item){

    item.addEventListener("click",function(){

        menuItems.forEach(function(nav){

            nav.classList.remove("active");

        });

        this.classList.add("active");

    });

});

/*=====================================
        NOTIFICATION BADGE
=====================================*/

const notification = document.querySelector(".notification");

if(notification){

    notification.addEventListener("click",function(){

        alert(
            "Security Notifications\n\n" +
            "• 17 Security Alerts\n" +
            "• 482 Threats Blocked Today\n" +
            "• Firewall Running Normally\n" +
            "• Zero Trust Score : 96%"
        );

    });

}

/*=====================================
        DASHBOARD COUNTER
=====================================*/

function animateCounter(element){

    const target = Number(
        element.innerText.replace(/[^0-9]/g,"")
    );

    if(isNaN(target)) return;

    let count = 0;

    const speed = Math.max(10,target/80);

    const timer = setInterval(function(){

        count += speed;

        if(count >= target){

            count = target;

            clearInterval(timer);

        }

        element.innerText = Math.floor(count);

    },20);

}

document.querySelectorAll(
".card-info h2,.metric-card h2,.health-card h1"
).forEach(function(el){

    animateCounter(el);

});

/*=====================================
        WELCOME MESSAGE
=====================================*/

setTimeout(function(){

    console.log(
        "Welcome to IBM Zero Trust Security Gateway"
    );

},1000);
/*=====================================================
        SCRIPT.JS PART 3
        REAL-TIME SECURITY CHART
======================================================*/

/*=====================================
        CHART.JS
=====================================*/

const chartCanvas = document.getElementById("securityChart");

if(chartCanvas){

    const ctx = chartCanvas.getContext("2d");

    const securityChart = new Chart(ctx,{

        type:"line",

        data:{

            labels:[
                "09:00",
                "10:00",
                "11:00",
                "12:00",
                "13:00",
                "14:00",
                "15:00"
            ],

            datasets:[

                {

                    label:"Threats Blocked",

                    data:[18,25,20,30,24,35,28],

                    borderColor:"#33659A",

                    backgroundColor:"rgba(111,166,208,0.20)",

                    borderWidth:3,

                    fill:true,

                    tension:0.4,

                    pointRadius:5,

                    pointBackgroundColor:"#33659A"

                }

            ]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    labels:{

                        color:"#183B5A",

                        font:{
                            size:14,
                            weight:"bold"
                        }

                    }

                }

            },

            scales:{

                x:{

                    ticks:{
                        color:"#183B5A"
                    },

                    grid:{
                        color:"#C7E4F2"
                    }

                },

                y:{

                    beginAtZero:true,

                    ticks:{
                        color:"#183B5A"
                    },

                    grid:{
                        color:"#C7E4F2"
                    }

                }

            }

        }

    });

/*=====================================
      LIVE CHART UPDATE
=====================================*/

    setInterval(function(){

        const value = Math.floor(Math.random()*20)+20;

        securityChart.data.datasets[0].data.shift();

        securityChart.data.datasets[0].data.push(value);

        const currentTime = new Date().toLocaleTimeString([],{

            hour:"2-digit",

            minute:"2-digit"

        });

        securityChart.data.labels.shift();

        securityChart.data.labels.push(currentTime);

        securityChart.update();

    },5000);

}
/*=====================================================
        SCRIPT.JS PART 4
   ALERTS • LIVE STATUS • WATSON ASSISTANT
======================================================*/

/*=====================================
      LIVE SECURITY ALERTS
=====================================*/

const alertMessages = [

    "Firewall Signature Updated Successfully",

    "New Endpoint Connected Securely",

    "Suspicious Login Attempt Blocked",

    "Identity Verification Completed",

    "VPN Tunnel Secured",

    "Threat Intelligence Database Updated",

    "Multi-Factor Authentication Verified",

    "Security Scan Completed"

];

const threatFeed = document.querySelector(".threat-feed");

if(threatFeed){

    setInterval(function(){

        const randomMessage = alertMessages[
            Math.floor(Math.random()*alertMessages.length)
        ];

        const newAlert = document.createElement("div");

        newAlert.className = "feed-item";

        newAlert.innerHTML = `

            <h4>Live Security Event</h4>

            <p>${randomMessage}</p>

            <small>Just Now</small>

        `;

        threatFeed.prepend(newAlert);

        if(threatFeed.children.length > 6){

            threatFeed.removeChild(threatFeed.lastElementChild);

        }

    },8000);

}

/*=====================================
      NOTIFICATION COUNTER
=====================================*/

const notificationCount = document.querySelector(".notification span");

if(notificationCount){

    let count = 5;

    setInterval(function(){

        count++;

        notificationCount.innerText = count;

    },15000);

}

/*=====================================
      WATSON BUTTON
=====================================*/

const watsonButton = document.querySelector(".watson-btn");

if(watsonButton){

    watsonButton.addEventListener("click",function(){

        alert(

`IBM Watson Assistant

Status : Online

✔ Threat Investigation

✔ Security Recommendations

✔ Identity Verification

✔ Incident Response

✔ Zero Trust Guidance`

        );

    });

}

/*=====================================
      STATUS BADGE ANIMATION
=====================================*/

const statusBadges = document.querySelectorAll(".status");

setInterval(function(){

    statusBadges.forEach(function(badge){

        badge.style.opacity = "0.6";

        setTimeout(function(){

            badge.style.opacity = "1";

        },400);

    });

},3000);

/*=====================================
      NETWORK HEALTH UPDATE
=====================================*/

const healthCards = document.querySelectorAll(".health-card h1");

setInterval(function(){

    if(healthCards.length >= 4){

        healthCards[1].innerText =
            Math.floor(Math.random()*80)+430;

        healthCards[3].innerText =
            Math.floor(Math.random()*3)+97+"%";

    }

},7000);
/*=====================================================
        SCRIPT.JS PART 5
      FINAL INITIALIZATION
======================================================*/

/*=====================================
      DASHBOARD ANIMATION
=====================================*/

const cards = document.querySelectorAll(
".card, .panel, .health-card, .metric-card, .compliance-card"
);

cards.forEach(function(card,index){

    card.style.opacity="0";

    card.style.transform="translateY(30px)";

    setTimeout(function(){

        card.style.transition="all 0.6s ease";

        card.style.opacity="1";

        card.style.transform="translateY(0)";

    },index*120);

});

/*=====================================
      SMOOTH SCROLL
=====================================*/

document.querySelectorAll('a[href^="#"]').forEach(function(anchor){

    anchor.addEventListener("click",function(e){

        e.preventDefault();

        const target=document.querySelector(this.getAttribute("href"));

        if(target){

            target.scrollIntoView({

                behavior:"smooth"

            });

        }

    });

});

/*=====================================
      OPTIONAL LOGOUT BUTTON
=====================================*/

const logoutBtn=document.getElementById("logoutBtn");

if(logoutBtn){

    logoutBtn.addEventListener("click",function(){

        if(confirm("Do you want to logout?")){

            dashboard.style.display="none";

            loginScreen.style.display="flex";

            loginScreen.style.opacity="1";

            userId.value="";

            password.value="";

            loginError.textContent="";

        }

    });

}

/*=====================================
      STARTUP MESSAGE
=====================================*/

console.log("======================================");

console.log(" IBM ZERO TRUST SECURITY GATEWAY ");

console.log(" Frontend Initialized Successfully ");

console.log(" Version : 2026 ");

console.log("======================================");

/*=====================================
      SYSTEM STATUS
=====================================*/

setTimeout(function(){

    console.log("✔ Identity Verification Active");

    console.log("✔ Zero Trust Policy Enabled");

    console.log("✔ Firewall Protected");

    console.log("✔ Threat Monitoring Running");

    console.log("✔ IBM Watson Ready");

},1500);

/*=====================================
      CLOSE DOMCONTENTLOADED
=====================================*/

});