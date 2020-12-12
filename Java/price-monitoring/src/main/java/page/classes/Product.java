package page.classes;

import entities.LocationEntity;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import repositories.location.LocationRepository;
import util.enums.ProductType;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.inject.Inject;
import javax.inject.Named;
import java.io.Serializable;
import java.util.List;

@Named
@RequestScoped
@Getter
@Setter
public class Product implements Serializable {
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    @Inject
    private LocationRepository locationRepository;

    private List<LocationEntity> locationEntities;

    private LocationEntity location;
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

    }
}
