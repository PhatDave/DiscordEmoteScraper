function runGrabber() {
    var allemotes = {}
    let emoteTray = $("div[class^=drawerSizingWrapper]")
    let scrolly = $(".scroller-2MALzE")
    var scroll = 0
    var scrollIncrement = 100
    var intervalId
    emoteTray.setAttribute("style", "width: 100%; height: 100%")

    function addEmotes() {
        let emotes = document.getElementsByClassName("emojiItem-277VFM")
        let anyAdded = false
        for (let i = 0; i < emotes.length; i++) {
            let emote = emotes[i]
            let command = emote.getAttribute("data-name")
            let emoteImg = emote.querySelector("img")
            if (emoteImg == undefined) {
                continue
            }
            let imgSource = emoteImg.getAttribute("src")
            if (allemotes[imgSource] === undefined) {
                allemotes[imgSource] = command
                anyAdded = true
            }
        }
        return anyAdded || emotes.length == 0
    }

    function addEmotesAndScroll() {
        if (addEmotes()) {
            console.log(Object.keys(allemotes).length)
            scroll += scrollIncrement
            scrolly.scroll(0, scroll)
        } else {
            console.log(Object.keys(allemotes).length)
            console.log("Done!")
            console.log(allemotes)
            clearInterval(intervalId)
        }
    }

    if (emoteTray != null && emoteTray != undefined) {
        intervalId = setInterval(addEmotesAndScroll, 250)
    }
}
runGrabber()