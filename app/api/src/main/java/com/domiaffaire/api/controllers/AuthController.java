package com.domiaffaire.api.controllers;

import com.domiaffaire.api.dto.*;
import com.domiaffaire.api.entities.User;
import com.domiaffaire.api.exceptions.UserNotFoundException;
import com.domiaffaire.api.exceptions.WrongCodeAccountantException;
import com.domiaffaire.api.mappers.Mapper;
import com.domiaffaire.api.repositories.UserRepository;
import com.domiaffaire.api.services.AuthService;
import com.domiaffaire.api.services.DomiAffaireServiceImpl;
import com.domiaffaire.api.services.jwt.UserService;
import com.domiaffaire.api.utils.JwtUtil;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.*;


@RestController
@RequiredArgsConstructor
@Slf4j
@RequestMapping("/api/auth")
public class AuthController {
    private final AuthService authService;
    private final AuthenticationManager authenticationManager;
    private final UserService userService;
    private final JwtUtil jwtUtil;
    private final UserRepository userRepository;
    private Set<String> tokenBlacklist = new HashSet<>();
    private final DomiAffaireServiceImpl service;

    @GetMapping("/{email}")
    public ResponseEntity<?> findClientByEmail(@PathVariable String email){
        try {
            User client = service.findUserByEmail(email);
            return ResponseEntity.ok(client);
        } catch (UserNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("{\"message\":\"" + e.getMessage() + "\"}");
        }
    }


    @PostMapping(value = "/signup", consumes = {MediaType.MULTIPART_FORM_DATA_VALUE})
    public ResponseEntity<?> createCustomer(@RequestPart("image") MultipartFile file,
                                            @RequestPart("signupRequest") @Valid SignupRequest signupRequest) {
        if (authService.hasUserWithEmail(signupRequest.getEmail())) {
            return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).body("{\"message\":\"Email already exists\"}");
        }

        try {
            byte[] imageBytes = file.getBytes();
            User createdUser = authService.createUser(signupRequest, imageBytes);
            if (createdUser != null) {
                return ResponseEntity.status(HttpStatus.CREATED).body("{\"message\":\"Account created successfully\"}");
            } else {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("{\"message\":\"Failed to create user\"}");
            }
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("{\"message\":\"Failed to process image file.\"}");
        } catch (WrongCodeAccountantException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("{\"message\":\"Code accountant does not match.\"}");
        }
    }




    @PostMapping("/login")
    public ResponseEntity<?> createAuthenticationToken(@RequestBody AuthenticationRequest authenticationRequest) {
        try {
            authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(authenticationRequest.getEmail(), authenticationRequest.getPwd()));
            final UserDetails userDetails = userService.userDetailsService().loadUserByUsername(authenticationRequest.getEmail());
            Optional<User> optionalUser = userRepository.findFirstByEmail(userDetails.getUsername());
            final String jwt = jwtUtil.generateToken(userDetails);

            AuthenticationResponse authenticationResponse = new AuthenticationResponse();
            if (optionalUser.isPresent()) {
                if(!optionalUser.get().isEnabled())
                    return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("{\"message\":\"Account is not enabled\"}");
                authenticationResponse.setJwt(jwt);
                authenticationResponse.setUserId(optionalUser.get().getId());
                authenticationResponse.setUserRole(optionalUser.get().getUserRole());
                return ResponseEntity.ok(authenticationResponse);
            } else {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("{\"message\":\"Invalid username or password.\"}");
            }
        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("{\"message\":\"Invalid username or password.\"}");
        }
    }



    @GetMapping("/clients")
    public ResponseEntity<List<User>> getAllUsers(){
        List<User> users = userRepository.findAll();
        return ResponseEntity.ok(users);
    }








}