package com.domiaffaire.api.services;

import com.domiaffaire.api.dto.SignupRequest;
import com.domiaffaire.api.entities.User;
import com.domiaffaire.api.enums.UserRole;
import com.domiaffaire.api.exceptions.WrongCodeAccountantException;
import com.domiaffaire.api.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.BeanUtils;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService{
    private  final UserRepository userRepository;

    @Override
    public User createUser(SignupRequest signupRequest, byte[] imageBytes) throws WrongCodeAccountantException {
        if (signupRequest.getRole().equals(UserRole.CLIENT.toString())) {
            User client = new User();
            client.setEmail(signupRequest.getEmail());
            client.setFirstName(signupRequest.getFirstName());
            client.setLastName(signupRequest.getLastName());
            client.setPwd(new BCryptPasswordEncoder().encode(signupRequest.getPwd()));
            client.setImage(imageBytes);
            client.setPhoneNumber(signupRequest.getPhoneNumber());
            client.setBirthDate(signupRequest.getBirthDate());
            client.setUserRole(UserRole.CLIENT);
            client.setEnabled(true);
            User createdClient = userRepository.save(client);
            User createdUser = new User();
            BeanUtils.copyProperties(createdClient, createdUser);
            return createdUser;
        } else if (signupRequest.getRole().equals(UserRole.ACCOUNTANT.toString())) {
            User comptable = new User();
            comptable.setEmail(signupRequest.getEmail());
            comptable.setFirstName(signupRequest.getFirstName());
            comptable.setLastName(signupRequest.getLastName());
            comptable.setPwd(new BCryptPasswordEncoder().encode(signupRequest.getPwd()));
            comptable.setImage(imageBytes);
            comptable.setPhoneNumber(signupRequest.getPhoneNumber());
            comptable.setCode(signupRequest.getCode());
            comptable.setUserRole(UserRole.ACCOUNTANT);
            comptable.setEnabled(true);
            if ("abcd".equals(signupRequest.getCode())) {
                User createdAccountant = userRepository.save(comptable);
                User createdUser = new User();
                BeanUtils.copyProperties(createdAccountant, createdUser);
                return createdUser;
            } else {
                throw new WrongCodeAccountantException("Code accountant does not match");
            }
        } else {
            return null;
        }
    }


    @Override
    public boolean hasUserWithEmail(String email) {
        return userRepository.findFirstByEmail(email).isPresent();
    }



}
