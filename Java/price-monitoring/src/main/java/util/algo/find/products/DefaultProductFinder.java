package util.algo.find.products;

import entities.ProductEntity;
import lombok.NoArgsConstructor;
import page.classes.Information;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import java.util.LinkedList;
import java.util.List;

@NoArgsConstructor
@Named
@ApplicationScoped
public class DefaultProductFinder {
    @Inject
    private EntityManager entityManager;

    public List<ProductEntity> prepareQuery(Information information){
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();

        CriteriaQuery<ProductEntity> query = criteriaBuilder.createQuery(ProductEntity.class);
        Root<ProductEntity> root = query.from(ProductEntity.class);

        List<Predicate> predicates = new LinkedList<>();
        predicates.add(criteriaBuilder.equal(root.get("location"), information.getProductEntity().getLocation()));
        predicates.add(criteriaBuilder.equal(root.get("type"), information.getProductEntity().getType()));
        predicates.add(criteriaBuilder.ge(root.get("size"), information.getProductEntity().getSize()));

        if(information.getSelectedFields().isRooms()){
            predicates.add(criteriaBuilder.equal(root.get("numberOfRooms"), information.getProductEntity().getNumberOfRooms()));
        }

        if(information.getSelectedFields().isYearOfConstruction()){
            predicates.add(criteriaBuilder.ge(root.get("yearOfConstruction"), information.getProductEntity().getYearOfConstruction()));
        }

        if(information.getSelectedFields().isNumberOfFloors()){
            predicates.add(criteriaBuilder.equal(root.get("numberOfFloors"), information.getProductEntity().getNumberOfFloors()));
        }

        if(information.getSelectedFields().isFloorNumber()){
            predicates.add(criteriaBuilder.equal(root.get("floorNumber"), information.getProductEntity().getFloorNumber()));
        }

        Predicate[] predicates1;
        predicates1 = predicates.toArray(new Predicate[0]);

        query.select(root).where(criteriaBuilder.and(predicates1));

        return entityManager.createQuery(query).getResultList();
    }
}
