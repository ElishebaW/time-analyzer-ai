package com.snake.game.entity;

import lombok.Getter;
import lombok.Setter;
import java.util.List;
import com.snake.game.entity.User;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.OneToMany;

@Entity
@Table(name = "tasks")
@Getter
@Setter
public class Task {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String description;
    private String status;
    private String priority;
    private String dueDate;
    private String assignedTo;
    private String createdAt;
    private String updatedAt;


    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
}


