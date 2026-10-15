package com.domiaffaire.api.services;

import com.domiaffaire.api.dto.ChangePasswordRequest;
import com.domiaffaire.api.dto.SignupRequest;
import com.domiaffaire.api.entities.User;
import com.domiaffaire.api.enums.UserRole;
import com.domiaffaire.api.exceptions.WrongCodeAccountantException;
import com.domiaffaire.api.exceptions.WrongPasswordException;
import com.domiaffaire.api.mappers.Mapper;
import com.domiaffaire.api.repositories.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.util.Date;
import java.util.Optional;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;



class DomiAffaireServiceImplTest {

    //which service we want to test
    @InjectMocks
    private DomiAffaireServiceImpl domiAffaireService;

    //declare the dependecies
    @Mock
    private Mapper mapper;
    @Mock
    private UserRepository userRepository;
    @Mock
    private BCryptPasswordEncoder passwordEncoder;

    @InjectMocks
    private AuthServiceImpl authService;


    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void should_successfully_change_password() throws WrongPasswordException {
        String userId = "user123";
        String oldPassword = "oldPassword";
        String newPassword = "newPassword";

        User user = new User();
        user.setId(userId);
        user.setPwd(new BCryptPasswordEncoder().encode(oldPassword));

        ChangePasswordRequest changePasswordRequest = new ChangePasswordRequest();
        changePasswordRequest.setOldPassword(oldPassword);
        changePasswordRequest.setNewPassword(newPassword);
        changePasswordRequest.setConfirmPassword(newPassword);

        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        when(userRepository.save(any(User.class))).thenAnswer(invocation -> invocation.getArgument(0));

        // When
        domiAffaireService.changePassword(userId, changePasswordRequest);

        // Then
        assertTrue(new BCryptPasswordEncoder().matches(newPassword, user.getPwd()));
    }


    @Test
    public void should_throw_wrong_password_exception_when_old_password_does_not_match() {
        // Given
        String userId = "user123";
        String oldPassword = "incorrectOldPassword";
        String newPassword = "newPassword";

        User user = new User();
        user.setId(userId);
        user.setPwd(new BCryptPasswordEncoder().encode("oldPassword"));

        ChangePasswordRequest changePasswordRequest = new ChangePasswordRequest();
        changePasswordRequest.setOldPassword(oldPassword);
        changePasswordRequest.setNewPassword(newPassword);

        when(userRepository.findById(userId)).thenReturn(Optional.of(user));

        // When & Then
        assertThrows(WrongPasswordException.class, () -> domiAffaireService.changePassword(userId, changePasswordRequest));
    }

    @Test
    void testCreateClientUser() throws WrongCodeAccountantException {
        SignupRequest signupRequest = new SignupRequest();
        signupRequest.setRole(UserRole.CLIENT.toString());
        signupRequest.setEmail("wassim.ouertani@gmail.com");
        signupRequest.setFirstName("Wassim");
        signupRequest.setLastName("Ouertani");
        signupRequest.setPwd("Aa7_$&ddzns4455Hfd");
        signupRequest.setPhoneNumber("25741818");
        signupRequest.setBirthDate(new Date());

        byte[] imageBytes = new byte[0];

        User savedUser = new User();
        savedUser.setId("user1");
        savedUser.setEmail(signupRequest.getEmail());

        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        User createdUser = authService.createUser(signupRequest, imageBytes);

        assertNotNull(createdUser);
        assertEquals("wassim.ouertani@gmail.com", createdUser.getEmail());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    void testCreateAccountantUserWithCorrectCode() throws WrongCodeAccountantException {
        SignupRequest signupRequest = new SignupRequest();
        signupRequest.setRole(UserRole.ACCOUNTANT.toString());
        signupRequest.setEmail("accountant@example.com");
        signupRequest.setFirstName("Accountant");
        signupRequest.setLastName("User");
        signupRequest.setPwd("password");
        signupRequest.setPhoneNumber("90842850");
        signupRequest.setCode("abcd");

        byte[] imageBytes = new byte[0];

        User savedUser = new User();
        savedUser.setId("user2");
        savedUser.setEmail(signupRequest.getEmail());

        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        User createdUser = authService.createUser(signupRequest, imageBytes);

        assertNotNull(createdUser);
        assertEquals("accountant@example.com", createdUser.getEmail());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    void testCreateAccountantUserWithWrongCode() {
        SignupRequest signupRequest = new SignupRequest();
        signupRequest.setRole(UserRole.ACCOUNTANT.toString());
        signupRequest.setEmail("accountant@example.com");
        signupRequest.setFirstName("Accountant");
        signupRequest.setLastName("User");
        signupRequest.setPwd("password");
        signupRequest.setPhoneNumber("1234567890");
        signupRequest.setCode("wrongcode");

        byte[] imageBytes = new byte[0];

        assertThrows(WrongCodeAccountantException.class, () -> {
            authService.createUser(signupRequest, imageBytes);
        });

        verify(userRepository, times(0)).save(any(User.class));
    }

}