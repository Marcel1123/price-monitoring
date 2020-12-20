package page.classes;

import entities.LocationEntity;
import entities.ProductEntity;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import repositories.location.LocationRepository;
import util.algo.find.products.DefaultProductFinder;
import util.enums.ProductType;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.inject.Inject;
import javax.inject.Named;
import java.io.Serializable;
import java.util.List;
import java.util.UUID;

@Named
@RequestScoped
@Getter
@Setter
public class Product implements Serializable {
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    @Inject
    private LocationRepository locationRepository;
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    @Inject
    private DefaultProductFinder productFinder;

    private List<LocationEntity> locationEntities;

    private String location;
    private int numberOfRooms;
    private ProductType type;
    private double size;
    private int floorNumber;
    private int numberOfFloors;
    private int yearOfConstruction;

    @PostConstruct
    public void init(){
        locationEntities = locationRepository.getAll();
    }

    public void estimation(){
        ProductEntity productEntity = new ProductEntity();
        productEntity.setType(type);
        productEntity.setLocation(locationRepository.getById(UUID.fromString(location)));
        List<ProductEntity> productEntities = productFinder.prepareQuery(productEntity);
        System.out.println(productEntities);
    }
}
