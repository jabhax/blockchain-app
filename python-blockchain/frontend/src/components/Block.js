import React, {useState} from 'react';
import {Button} from 'react-bootstrap';
import {MILLI_SECONDS_PY} from '../config';
import Transaction from './Transaction';

function ToggleTransactionDisplay({block}) {
    const [displayTransaction, setDisplayTransaction] = useState(false);
    const {data} = block;
    const toggleDisplayTransaction = () => {
        setDisplayTransaction(!displayTransaction);
    }

    if (displayTransaction) {
        return (
            <div>
                {
                    data.map(transaction => (
                        <div className='Transaction'>
                            <hr/>
                            <Transaction transaction={transaction}/>
                        </div>
                    ))
                }
                <br/>
                <Button variant='danger' size='sm' onClick={toggleDisplayTransaction}>-</Button>
            </div>
        )
    }
    return (
        <div>
            <br/>
            <Button variant='danger' size='sm' onClick={toggleDisplayTransaction}>+</Button>
        </div>
    )
}

function Block({block}) {
    const {timestamp, hash} = block;
    const hashDisplay = `${hash.substring(0, 15)}...`;
    const timestampDisplay = new Date(timestamp / MILLI_SECONDS_PY).toLocaleString();

    return (
        <div className='Block'>
            <div>Hash: {hashDisplay}</div>
            <div>Timestamp: {timestampDisplay}</div>
            <ToggleTransactionDisplay block={block} />
        </div>
    )
}

export default Block;
