import {createStore} from "vuex";

const store = createStore({
    state() {
        return {
            parameters: [],
            plants: []
        }
    },
    mutations: {
        SET_PARAMETERS(state, new_parameters) {
            state.parameters = new_parameters;
        },
        SET_PLANTS(state, new_plants) {
            state.plants = new_plants;
        }
    }
})

export default store