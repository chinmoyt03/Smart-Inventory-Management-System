<template>
  <div>
    <!-- Heading and the input field for text -->
    <h1>AI Shopping List </h1>  
    <input v-model="textInput" placeholder="Type your shopping list here">
    <button @click="generateList">Generate List</button>
    
    <div v-if="transcribedText">
      <h2>Generated Text from the input:</h2>
      <!-- display the value of transcribedText  -->
      <p>{{ transcribedText }}</p>                                
                      
    </div>

    <!-- display the shopping list  -->
    <div v-if="shoppingList">
      <h2>Shopping List:</h2>
      <ul>
        <li v-for="(quantity, item) in shoppingList" :key="item">
          {{ quantity }} x {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";    // import axios to interact with the backend server

export default {
  data() {
    return {
      textInput: "",
      transcribedText: "",
      shoppingList: null
    };
  },

  methods: {
    generateList() {
      // Send text input to the server for processing
      axios
        .post("http://localhost:5000/ab", { text: this.textInput })
        .then(response => {
          this.transcribedText = response.data.transcribedText;
          this.shoppingList = response.data.shoppingList;
        })
        .catch(error => console.error("Error: ", error));
    }
  }
};
</script>

<!-- CSS -->
<style>
button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #2f6bbe; 
  color: white;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
  border-radius: 25px;
}

button:hover {
  background-color: #7daa13; 
}
</style>
