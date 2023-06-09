import React, { useContext, useState } from 'react';
import { StyleSheet, View, Image, useWindowDimensions, Pressable, Alert, Text, TouchableOpacity, ScrollView, VirtualizedList } from 'react-native';
import { Context } from "./globalContext"

// import React, {useState, useContext} from 'react'
// import {StyleSheet, Text, View, Image, useWindowDimensions, Pressable, Alert} from 'react-native';
import {TextInput} from 'react-native-paper'
import Logo from '../assets/Images/newlogo.png'

function SignIn({ navigation, route, props}) {
    const {height} = useWindowDimensions()
    // const[password, setPassword] = useState("")
    // const[email, setEmail] = useState("")
    const globalContext = useContext(Context)
    const { setIsLoggedIn, domain, userObj, setUserObj } = globalContext;
  
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
  
    function InsertData() {
  
      setError("")
  
      let body = JSON.stringify({
        'username': email.toLowerCase(),
        'password': password
      })
  
      fetch(`${domain}/api/auth/login-user/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body:body
        })
        .then(res => {
          if (res.ok) {
            return res.json()
          } else {
            setError("Invalid Credentials")
            throw res.json()
          }
        })
        .then(json => {
          console.log(json) 
          setUserObj(json)
        //   setToken(json.token)
          setIsLoggedIn(true)
        })
        .catch(error => {
          Alert.alert("Account Does Not Exist")
        })
  
    }
  
    // const InsertData = async () => {
    //     let obj1
    //     let obj2
    //     let shouldcontinue = true
    //     fetch(`http://10.21.183.52/login/${email}`, {
    //         method: "POST",
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'X-CSRFToken': csrftoken
    //         }})
    //         .then(res => res.text())    
    //         .then(data => {
    //             obj1 = data
    //             console.log(data)
    //             if(!("email" in data)) {
    //                 Alert.alert("Account Does Not Exist.")
    //                 shouldcontinue = false
    //                 setEmail("")
    //                 setPassword("")
    //             }})
    //             .catch(err => {
    //                 shouldcontinue = false
    //                 Alert.alert("Account Does Not Exist.")
    //                 console.log("Error", err)})

        // fetch(`http://10.21.183.52/api/userspass/${password}`, {
        //     method: "POST",
        //     headers: {
        //         'Content-Type': 'application/json'
        //     }})
        // .then(res => res.json())    
        // .then(data => {
        //     obj2 = data
        //     console.log(data)
        //     if(!("password" in data)) {
        //         shouldcontinue = false
        //         Alert.alert("Account Does Not Exist.")
        //         setEmail("")
        //         setPassword("")
        //     }})
        // .catch(err => {
        //     shouldcontinue = false
        //     console.log("Error", err)})

        // if (shouldcontinue == true) {
        //     props.navigation.navigate("ListingPage")
        // }
    // }
    // useEffect(() => {
    //     onLoad();
    //   },[isAuthenticated]);

    return (
        <View>
        <ScrollView>
        <View style = {styles.root}>
            <Image source = {Logo} style = {[styles.logo, {height: height * 0.3}]} resizeMode = "contain" />
        </View>
        <View>
            <Text style = {styles.header}>
                Log In
            </Text>
            <Text style = {styles.subheader}>
                Please sign in to continue.
            </Text>
            <TextInput style = {styles.inputStyle}
                label = "Email"
                value = {email}
                textContentType="username"
                onChangeText={text => setEmail(text)}
            />
            <TextInput style = {styles.inputStyle}
                label = "Password"
                value = {password}
                secureTextEntry = {true}
                textContentType="password"
                onChangeText={text => setPassword(text)}

            />
        </View>
        <Pressable style = {styles.btn} onPress = {() => InsertData()}>
        <Text style = {styles.txt}>
            Sign In
        </Text>
        </Pressable>
        <Pressable style = {[styles.altbtn, {marginBottom: 100}]} onPress = {() => navigation.navigate("PasswordReset")}>
        <Text style = {styles.alttxt}>
            Forgot Password?
        </Text>
        </Pressable>
        <View>
        <Pressable style = {styles.altbtn} onPress = {() => navigation.navigate("CreateAccount")}>
        <Text style = {styles.alttxt}>
            Don't have an account?
            <Text style = {{color: 'blue'}}> Create One.</Text>
        </Text>
        </Pressable>
        </View>
        </ScrollView> 
        </View>
    )
}

const styles = StyleSheet.create({
    header : {
        fontWeight : 'bold',
        fontSize : 35,
        marginLeft : 10,
    },
    subheader : {
        fontWeight : 'bold',
        marginLeft : 10,
        marginBottom : 30,
        color : 'gray'
    },
    inputStyle: {
        backgroundColor: 'white',
        margin : '3%',
        borderColor: '#e8e8e8',
        borderRadius: 5,
        paddingHorizontal: 10,
        marginVertical: 5,
    },
    btn : {
        backgroundColor : '#87CEEB',
        margin : '3%',
        padding: 15,
        marginVertical: 5,
        alignItems: 'center',
        borderRadius: 5,
    },
    altbtn : {
        margin : '3%',
        padding: 15,
        marginVertical: 5,
        alignItems: 'center',
        borderRadius: 5,
    },
    alttxt : {
        color : 'grey',
    },
    txt : {
        color : 'black',
    },
    root : {
        alignItems: 'center',
        padding: 20,    
    },
    logo : {
        marginTop : 20,
        width : '70%',
        maxWidth: 300,
        maxHeight: 200,
    }
})
export default SignIn

// get images to show up and be stored in firebase in the create post and edit post
//validate social security
// whatevers left for geolocation page
// fix dates (dont let expired posts be shown and show in a correct format and save completed dates correctly)
// fix location (show locations correctly and only allow people within a certain vicinity to see the posts)
//logout functionality
// forgot password
// ui changes
// fix VirtualizedList
// terms of service page
// validate forms
//average rating

//nathan: firebase
//jonathan: social security validation
//vijay: ui changes, fix dates and locations

