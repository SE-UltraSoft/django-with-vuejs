<template>
  <div class="login-container">
    <!-- <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="login-form" auto-complete="on"
      label-position="left"> -->
    <el-form ref="ruleForm" :model="ruleForm" :rules="rules" class="login-form" auto-complete="on" label-position="left">

      <div class="title-container">
        <h3 class="title">Register</h3>
      </div>

      <el-form-item prop="uid">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="uid"
          v-model="ruleForm.uid"
          placeholder="学号"
          name="uid"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="ruleForm.username"
          placeholder="用户名"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>
      
      <el-form-item prop="email">
        <span class="svg-container">
          <i class="el-icon-message"></i>
        </span>
        <el-input placeholder="邮箱" v-model="ruleForm.email"></el-input>
      </el-form-item>

      <el-form-item prop="ecode">
        <el-row style="text-align: cener">
          <el-col :span="2">
            <span class="svg-container">
              <i class="el-icon-edit-outline"></i>
            </span>
          </el-col>
          <el-col :span="16" style="margin-left: -5px">
            <el-input placeholder="验证码" v-model="ruleForm.ecode"></el-input>
          </el-col>
          <el-col :span="6" style="margin-top: 5px">
            <el-button @click="mailVertify">发送验证码</el-button>
          </el-col>
        </el-row>
      </el-form-item>
      

      <el-form-item prop="pass">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="pass"
          v-model="ruleForm.pass"
          :type="passwordType"
          placeholder="密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleSubmit"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <el-form-item prop="checkPass">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input type="password" placeholder="确认密码" v-model="ruleForm.checkPass" autocomplete="off"/>
      </el-form-item>

      <el-form-item>
        <!-- <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button> -->
         <el-button type="primary" style="width:100%;" 
          @click.native.prevent="submitForm('ruleForm')">注册</el-button>
      </el-form-item>
      
    </el-form>
  </div>
</template>

<script>
import { register } from '@/api/user'
  export default {
    data() {
      const validateUid = (rule, value, callback) => {
        if (value == '') {
          callback(new Error('请输入学号'))
        } else {
          callback()
        }
      }
      const validateUsername = (rule, value, callback) => {
        if (value == '') {
          callback(new Error('请输入用户名'))
        } else {
          callback()
        }
      }
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        ruleForm: {
          uid: '',
          username: '',
          email: '',
          ecode: '',
          pass: '',
          checkPass: '',
        },
        rules: {
          uid: [
            {require: true, validator: validateUid, trigger: 'blur'}
          ],
          username: [
            { require: true, validator: validateUsername, trigger: 'blur'}
          ],
          pass: [
            { require: true, validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱地址', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
          ]
        },
        passwordType: 'password'
      };
    },
    watch: {
      "ruleForm.uid": {
        handler(newVal){
          console.log("change")
          this.ruleForm.email = newVal + '@buaa.edu.cn'
        },
        deep: true
      }
    },
    methods: {
      mailVertify() {

      },

      showPwd() {
        if (this.passwordType === 'password') {
          this.passwordType = ''
        } else {
          this.passwordType = 'password'
        }
        this.$nextTick(() => {
          this.$refs.pass.focus()
        })
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            register(this.ruleForm).then(res => {
              alert('submit!');
              this.$router.push({ path: '/login' })
            }).catch(error => {
              alert(error)
            })

          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .labelterm {
    font-size: 18px;
    color: #fff;
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 50px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
