package com.wistron.witlab.model;

import java.util.Date;
import java.util.Objects;

// 一個Employee的類別, 用來作DTO (Data Tranfer Object)使用
public class Employee {
    private String id;
    private String firstName;
    private String lastName;
    private String deptId;
    private Date hireDate;
    private Date terminationDate;
    private Float wage = 0f;
    private Integer age = 0;
    private Boolean sex = false;


    /**
     * 沒有引數的Constructor, 做為一個DTO必需要有
     */
    public Employee(){

    }

    /**
     * Employee物件的constructor
     *
     * @param id Employee ID
     * @param firstName FirstName
     * @param lastName LastName
     * @param deptId Dept ID
     * @param hireDate Hire Date
     * @param wage Wage
     * @param sex Male (true) or Female (false)
     */
    public Employee(String id, String firstName, String lastName, String deptId, Date hireDate, Float wage, Boolean sex) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.deptId = deptId;
        this.hireDate = hireDate;
        this.wage = wage;
        this.sex = sex;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getDeptId() {
        return deptId;
    }

    public void setDeptId(String deptId) {
        this.deptId = deptId;
    }

    public Date getHireDate() {
        return hireDate;
    }

    public void setHireDate(Date hireDate) {
        this.hireDate = hireDate;
    }

    public Date getTerminationDate() {
        return terminationDate;
    }

    public void setTerminationDate(Date terminationDate) {
        this.terminationDate = terminationDate;
    }

    public Float getWage() {
        return wage;
    }

    public void setWage(Float wage) {
        this.wage = wage;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Boolean getSex() {
        return sex;
    }

    public void setSex(Boolean sex) {
        this.sex = sex;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee employee = (Employee) o;
        return Objects.equals(id, employee.id) &&
                Objects.equals(firstName, employee.firstName) &&
                Objects.equals(lastName, employee.lastName) &&
                Objects.equals(deptId, employee.deptId) &&
                Objects.equals(hireDate, employee.hireDate) &&
                Objects.equals(terminationDate, employee.terminationDate) &&
                Objects.equals(wage, employee.wage) &&
                Objects.equals(age, employee.age) &&
                Objects.equals(sex, employee.sex);
    }

    @Override
    public int hashCode() {

        return Objects.hash(id, firstName, lastName, deptId, hireDate, terminationDate, wage, age, sex);
    }

    @Override
    public String toString() {
        return "Employee{" +
                "id='" + id + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", deptId='" + deptId + '\'' +
                ", hireDate=" + hireDate +
                ", terminationDate=" + terminationDate +
                ", wage=" + wage +
                ", age=" + age +
                ", sex=" + sex +
                '}';
    }
}
