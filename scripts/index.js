
let input = document.getElementById("input");

document.getElementById("button").onclick = () => {
    fetch("/func", {
        method: "POST",
        body: input.value
    })
    .then(res => res.blob())
    .then(blob => {
        let url = URL.createObjectURL(blob);
        document.getElementById("image").src = url;
    });
}

document.getElementById("input").onkeydown = (e) => {
    if (e.key === "Enter") document.getElementById("button").click();
}
