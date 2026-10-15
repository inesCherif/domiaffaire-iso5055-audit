package com.domiaffaire.api.controllers;

import com.domiaffaire.api.dto.AuthenticationRequest;
import com.domiaffaire.api.dto.AuthenticationResponse;
import com.domiaffaire.api.dto.SignupRequest;
import com.domiaffaire.api.entities.User;
import com.domiaffaire.api.enums.UserRole;
import com.domiaffaire.api.exceptions.WrongCodeAccountantException;
import com.domiaffaire.api.repositories.UserRepository;
import com.domiaffaire.api.services.AuthService;
import com.domiaffaire.api.services.jwt.UserService;
import com.domiaffaire.api.utils.JwtUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.userdetails.UserDetailsService;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class AuthControllerTest {

    @Mock
    private AuthService authService;
    @Mock
    private AuthenticationManager authenticationManager;
    @Mock
    private UserService userService;
    @Mock
    private UserDetailsService userDetailsService;
    @Mock
    private JwtUtil jwtUtil;
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private AuthController authController;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void signupCreatesAccountWithoutEmailVerification() throws WrongCodeAccountantException {
        SignupRequest signupRequest = new SignupRequest();
        signupRequest.setRole(UserRole.CLIENT.toString());
        signupRequest.setEmail("client@example.com");

        User createdUser = new User();
        createdUser.setEmail("client@example.com");
        createdUser.setEnabled(true);

        when(authService.hasUserWithEmail("client@example.com")).thenReturn(false);
        when(authService.createUser(any(SignupRequest.class), any(byte[].class))).thenReturn(createdUser);

        ResponseEntity<?> response = authController.createCustomer(
                new MockMultipartFile("image", new byte[0]), signupRequest);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals("{\"message\":\"Account created successfully\"}", response.getBody());
    }

    @Test
    void signupRejectsExistingEmail() throws WrongCodeAccountantException {
        SignupRequest signupRequest = new SignupRequest();
        signupRequest.setEmail("client@example.com");

        when(authService.hasUserWithEmail("client@example.com")).thenReturn(true);

        ResponseEntity<?> response = authController.createCustomer(
                new MockMultipartFile("image", new byte[0]), signupRequest);

        assertEquals(HttpStatus.NOT_ACCEPTABLE, response.getStatusCode());
        verify(authService, never()).createUser(any(), any());
    }

    @Test
    void loginReturnsJwtForNewlyRegisteredUser() {
        User user = new User();
        user.setId("user1");
        user.setEmail("client@example.com");
        user.setPwd("encoded");
        user.setUserRole(UserRole.CLIENT);
        user.setEnabled(true);

        AuthenticationRequest request = new AuthenticationRequest();
        request.setEmail("client@example.com");
        request.setPwd("password");

        when(userService.userDetailsService()).thenReturn(userDetailsService);
        when(userDetailsService.loadUserByUsername("client@example.com")).thenReturn(user);
        when(userRepository.findFirstByEmail("client@example.com")).thenReturn(Optional.of(user));
        when(jwtUtil.generateToken(user)).thenReturn("jwt-token");

        ResponseEntity<?> response = authController.createAuthenticationToken(request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        AuthenticationResponse body = (AuthenticationResponse) response.getBody();
        assertNotNull(body);
        assertEquals("jwt-token", body.getJwt());
        assertEquals("user1", body.getUserId());
        assertEquals(UserRole.CLIENT, body.getUserRole());
    }

    @Test
    void loginRejectsBadCredentials() {
        AuthenticationRequest request = new AuthenticationRequest();
        request.setEmail("client@example.com");
        request.setPwd("wrong");

        when(authenticationManager.authenticate(any())).thenThrow(new BadCredentialsException("bad"));

        ResponseEntity<?> response = authController.createAuthenticationToken(request);

        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
        verify(jwtUtil, never()).generateToken(any());
    }
}
