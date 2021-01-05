package page.classes;

import entities.LocationEntity;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;
import lombok.SneakyThrows;
import repositories.location.LocationRepository;
import util.Redirect;
import util.algo.PriceEstimationAlgorithm;
import util.models.APIResponseModel;
import util.models.EstimatePriceModel;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.faces.context.FacesContext;
import javax.inject.Inject;
import javax.inject.Named;
import java.io.IOException;
import java.util.Map;

@Named
@RequestScoped
@Getter
@Setter
public class PriceEstimation {
    private EstimatePriceModel estimatePriceModel;
    private int estimatedPrice;
    private String locationCompleteName;

    @Inject
    @Getter(AccessLevel.PRIVATE)
    @Setter(AccessLevel.PRIVATE)
    private LocationRepository locationRepository;

    @PostConstruct
    @SneakyThrows
    public void init(){
        Map<String, Object> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getSessionMap();
        estimatePriceModel = (EstimatePriceModel) parameterValue.get("product");

        if(estimatePriceModel == null){
            Redirect.redirectToIndex();
        }

        PriceEstimationAlgorithm algorithm = new PriceEstimationAlgorithm();
        algorithm.makeAPICall(estimatePriceModel);
        estimatedPrice = algorithm.getApiResponseModel().getMessage();

        buildLocationName();
    }

    private void buildLocationName(){
        StringBuilder stringBuilder = new StringBuilder();

        LocationEntity locationEntity = locationRepository.getById(estimatePriceModel.getLocation_id());

        stringBuilder.append(locationEntity.getAddress());
        stringBuilder.append(", ");
        stringBuilder.append(locationEntity.getCity().getName());
        stringBuilder.append(", ");
        stringBuilder.append(locationEntity.getCity().getCountry());

        locationCompleteName = stringBuilder.toString();
    }
}
