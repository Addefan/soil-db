import {createStore} from "vuex";

const store = createStore({
    state() {
        return {
            count: 10
        }
    },
    mutations: {
        inc(state) {
            state.count++;
        }
    }
})

export default store