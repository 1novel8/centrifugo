import {Centrifuge} from 'centrifuge';
import {useState} from "react";


function App() {
    const [channel, setChannel] = useState('');
    const [cent, setCent] = useState(null)

    const [messages, setMessages] = useState([]);
    const connect = (e) => {
        e.preventDefault();
        const centrifuge = new Centrifuge("ws://localhost:8000/connection/websocket");

        centrifuge.on('connected', function (ctx) {
            console.log("подключено", ctx);
            console.log(ctx.data)
        });
        centrifuge.connect()

        setCent(centrifuge)
    }

    const subscribe = (e) => {
        e.preventDefault();
        const sub = cent.newSubscription(channel);
        sub.on('publication', function (ctx) {
            console.log("Получено сообщение:", ctx.data);
            setMessages((prev) => [...prev, JSON.stringify(ctx.data)]);
        });

        sub.subscribe();
    }

    return (
        <div className="App">
            <h1>Centrifugo</h1>
            <form onSubmit={connect}>
                <button type="submit">Подключиться к centrifugo</button>
            </form>
            <form onSubmit={subscribe}>
                <div>
                    <label>Channel:</label>
                    <input
                        type="text"
                        value={channel}
                        onChange={(e) => setChannel(e.target.value)}
                    />
                </div>
                <button type="submit">случать канал</button>
            </form>
            <div>
            </div>
            <div>
                <h3>Сообщения:</h3>
                <ul>
                    {messages.map((msg, index) => (
                        <li key={index}>{msg}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default App;