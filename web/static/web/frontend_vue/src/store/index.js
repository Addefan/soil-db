import {createStore} from "vuex";

const store = createStore({
    state() {
        return {
            parameters: [],
            plants: []
        }
    },
    mutations: {
        setParameters(state, new_parameters) {
            state.parameters = new_parameters;
        },
        setPlants(state, new_plants) {
            state.plants = new_plants;
        }
    }
})

export default store