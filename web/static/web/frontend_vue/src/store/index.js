import {createStore} from "vuex";

const store = createStore({
    state() {
        return {
            parameters: [],
            plants: []
        }
    },
    mutations: {
        SETPARAMETERS(state, new_parameters) {
            state.parameters = new_parameters;
        },
        SETPLANTS(state, new_plants) {
            state.plants = new_plants;
        }
    }
})

export default store