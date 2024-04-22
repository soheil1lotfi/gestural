const toggleMicBtn = document.getElementById('toggle-mic');
const toggleVideoBtn = document.getElementById('toggle-video');
const sendEmojiBtn = document.getElementById('send-emoji');
const raiseHandBtn = document.getElementById('raise-hand');
const overlayText = document.getElementById('overlay-text');
const raiseHandText = document.getElementById('raise-hand-text');

const thumbsUpBtn = document.getElementById('thumbs-up');
const thumbsDownBtn = document.getElementById('thumbs-down');
const peaceBtn = document.getElementById('peace');

toggleMicBtn.addEventListener('click', toggleMicrophone);
toggleVideoBtn.addEventListener('click', toggleVideo);
thumbsUpBtn.addEventListener('click', thumbsUp);
thumbsDownBtn.addEventListener('click', thumbsDown);
peaceBtn.addEventListener('click', peace);
raiseHandBtn.addEventListener('click', raiseHand);

let isHandRaised = false
let isMicrophoneOn = true
let isVideoOn = true
let gestureIcon = ''

setInterval(fetchCategoryName, 1000);

function toggleMicrophone() {
    let mic = document.getElementById('fa-mic')
    if (isMicrophoneOn) {
        toggleMicBtn.style.backgroundColor = 'red';
        mic.setAttribute('class', '')
        mic.setAttribute('class', 'fa fa-microphone-slash')
        isMicrophoneOn = false
    } else {
        toggleMicBtn.style.backgroundColor = '#282828';
        mic.setAttribute('class', '')
        mic.setAttribute('class', 'fa fa-microphone')
        isMicrophoneOn = true
    }
}
function toggleVideo() {
    let video = document.getElementById('fa-vid')
    if (isVideoOn) {
        toggleVideoBtn.style.backgroundColor = 'red';
        video.setAttribute('class', '')
        video.setAttribute('class', 'fa fa-eye-slash')
        isVideoOn = false
    } else {
        toggleVideoBtn.style.backgroundColor = '#282828';
        video.setAttribute('class', '')
        video.setAttribute('class', 'fa fa-video-camera')
        isVideoOn = true
    }
}
function fetchCategoryName(){
    fetch("/get_category_name")
        .then(res => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then(data => {
            if (data && data !== 'None') {
                switch (data) {
                    case 'Open_Palm':
                        raiseHand();
                        break;
                    case 'Thumb_Up':
                        thumbsUp();
                        break;
                    case 'Victory':
                        peace();
                        break;
                    case 'Thumb_Down':
                        thumbsDown();
                        break;
                    default:
                        break;
                }
            } else {
                console.log('nothing')
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}
function sendEmoji() {
    showOverlayText(gestureIcon)
}
function thumbsUp() {
    showOverlayText('👍🏻')
}
function thumbsDown() {
    showOverlayText('👎🏻')
}
function peace() {
    showOverlayText('✌🏻')
}
function raiseHand() {
    let raiseHandEmoji = document.getElementById('raise-hand')
    if (!isHandRaised) {
        raiseHandText.textContent = '✋🏻';
        raiseHandText.style.display = 'block';
        raiseHandEmoji.style.backgroundColor = 'dodgerblue';
        isHandRaised = true
    } else {
        raiseHandText.style.display = 'none'
        raiseHandEmoji.style.backgroundColor = '#282828';
        isHandRaised = false
    }
}
function showOverlayText(text) {
    overlayText.textContent = text;
    overlayText.style.display = 'block';

    setTimeout(() => {
        overlayText.style.display = 'none';
    }, 5000);
}