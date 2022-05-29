import React from 'react';
import { slide as Menu} from 'react-burger-menu';
import Dropdown from './Dropdown';
import './Mystyles.css';

export default props => {
    return (
        <Menu>
            <Dropdown/>
        </Menu>
    )
}