async function test_ws_con() {
    const ws=new WebSocket("ws://localhost:8000/api/video/ws/upload/")
    ws.onopen=(event)=>{
        console.log("ws open")
        console.log(event)
    }
    ws.onmessage=(event)=>{
        console.log("ws message")
        console.log(event)
    }
    ws.close=(event)=>{
        console.log("ws close")
        console.log(event)
    }
}

export default test_ws_con