<template>
  <div class="dashboard-container">
    <!-- <div class="dashboard-text">name: {{ name }}</div> -->
    <div>
      <el-input type="text" placeholder="输入URL" v-model="searchUrl" class="custom-input"> </el-input>
      <el-button type="primary" @click="search">搜索</el-button>
      <!-- <ul v-if="searchResults.length > 0">
        <li v-for="result in searchResults" :key="result.id">{{ result.title }}</li>
      </ul> -->
      <div class="search-results">
        <div class="card" v-for="result in searchResults" :key="result.id">
          <h3>{{ result.id }}</h3>
          <p>{{ result.url_title }}</p>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import {
  searchUrlA
} from "@/api/website";

export default {
  data() {
    return {
      searchUrl: 'cn.bing.com',
      searchResults: []
    };
  },
  methods: {
    search() {
      //这里可以编写发送请求获取搜索结果的逻辑,例如使用Axios或者Fetch API
      console.log(this.searchUrl);
      
      searchUrlA(this.searchUrl)  //.then(response => {}).catch(error => { this.$message.error('服务端异常, 搜索失败.'); })
      .then(res => {
        this.searchResults = res.searchResults
        console.log(this.searchResults);
      //   // console.log(res.code.list);
        setTimeout(() => {
          this.searchResults = res.searchResults
        }, 500)
      //   // if (res) {
      //   //   console.log(res.json());
      //   // }
      //   // else {
      //   //   console.log('OKK!');
      //   // }
      })
      .catch(err => {
        console.log(err)
        this.$message.error('服务端异常, 搜索失败.');
      });

      //假设这里获取到了搜索结果, 然后将结果存储在searchResults中
      //示例中用settimeout模拟异步请求
      // setTimeout(() => {
      //   this.searchResults = 
      //   [
      //     {id: 1, url_title: "搜索结果1"},
      //     {id: 2, url_title: "搜索结果2"},
      //     {id: 3, url_title: "搜索结果3"},  
      //   ];
      // }, 500)
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.custom {
  &-input {
    width:80%
  }
}

.search-results {
  display: flex;
  flex-direction: column; /*卡片竖向排列 */
  // align-items: center;
}

.card {
  width: 80%;
  padding: 20px;
  margin: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow:0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h3 {
  margin: 0 0 10px;
}

p {
  margin: 0;
}
</style>
