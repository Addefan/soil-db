import {createStore} from "vuex";

const store = createStore({
    state() {
        return {
            parameters: [],
            plants: []
        }
    },
    mutations: {}
})

export default store