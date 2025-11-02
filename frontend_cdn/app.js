// import Vue from 'vue'
import greeting from './greetings.js'

app = new Vue(
    {
        el: '#app',
        
        template:
        `
        <greeting></greeting>`,
        
        components: {
            greeting
        }

}
)