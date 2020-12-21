package util.database;

import entities.ProductEntity;

import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;

public class PredicateList {
    public static Predicate roomsPredicate(int rooms, CriteriaBuilder criteriaBuilder, Root<ProductEntity> root){
        return criteriaBuilder.equal(root.get("numberofrooms"), rooms);
    }

    public static Predicate floorNumberPredicate(int floorNumber, CriteriaBuilder criteriaBuilder, Root<ProductEntity> root){
        return criteriaBuilder.equal(root.get("floornumber"), floorNumber);
    }

    public static Predicate yearOfConstructionPredicate(int yearOfConstruction, CriteriaBuilder criteriaBuilder, Root<ProductEntity> root){
        return criteriaBuilder.equal(root.get("yearofcontruction"), yearOfConstruction);
    }

    public static Predicate numberOfFloorsPredicate(int numberOfFloors, CriteriaBuilder criteriaBuilder, Root<ProductEntity> root){
        return criteriaBuilder.equal(root.get("numberoffloors"), numberOfFloors);
    }
}
